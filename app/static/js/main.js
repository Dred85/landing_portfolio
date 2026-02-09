// Плавная отправка формы
document.getElementById("contactForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;
    const data = {
        name: form.name.value,
        email: form.email.value,
        message: form.message.value,
    };

    const responseEl = document.getElementById("response");

    try {
        const res = await fetch("/api/contact", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });
        const result = await res.json();
        responseEl.textContent = result.message;
        responseEl.className = "text-green-400";
        form.reset();
    } catch (err) {
        responseEl.textContent = "Ошибка отправки!";
        responseEl.className = "text-red-400";
    }
});

// Плавный скролл по ссылкам (если будут anchor)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e){
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({behavior: 'smooth'});
    });
});
