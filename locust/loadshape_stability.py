from locust import LoadTestShape, events

from locustfile import WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04

# -----------------
# PROMETHEUS EXPORTER FOR LOCUST
# -----------------
try:
    # Эти импорты будут работать после установки prometheus_client внутри контейнера locust
    from flask import Response
    from prometheus_client import (
        CollectorRegistry,
        Gauge,
        CONTENT_TYPE_LATEST,
        generate_latest,
    )

    _registry = CollectorRegistry()
    _locust_users_gauge = Gauge(
        "locust_users",
        "Number of running Locust users",
        registry=_registry,
    )

    @events.init.add_listener
    def _locust_init_prometheus(environment, **_kwargs):
        """
        Регистрируем /metrics на веб-приложении Locust и
        экспортируем текущий user_count.
        """
        if not environment.web_ui:
            return

        @environment.web_ui.app.route("/metrics")
        def metrics():  # type: ignore[func-name-mismatch]
            runner = environment.runner
            if runner is not None:
                # В разных версиях Locust есть user_count или список user_instances
                user_count = getattr(runner, "user_count", None)
                if user_count is None:
                    user_count = len(getattr(runner, "user_instances", []))
            else:
                user_count = 0

            _locust_users_gauge.set(user_count)
            return Response(generate_latest(_registry), mimetype=CONTENT_TYPE_LATEST)

except ModuleNotFoundError:
    # В локальной среде без prometheus_client просто не поднимаем /metrics
    pass


class LoadShape(LoadTestShape):
    """
    Stability / soak test с переключением сценарием
    """
    stages = [
        {"duration": 20, "users": 20, "spawn_rate": 1, "user_classes": [WebUser_UC01]},
        {"duration": 40, "users": 40, "spawn_rate": 1, "user_classes": [WebUser_UC03]},
        {"duration": 60, "users": 60, "spawn_rate": 1, "user_classes": [WebUser_UC04]},
        {"duration": 1800, "users": 60, "spawn_rate": 1}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
            run_time -= stage["duration"]

        return None
