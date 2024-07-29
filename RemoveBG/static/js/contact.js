document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('contact-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Impede o envio padrão do formulário
        
        // Exibe o carregamento e oculta a mensagem de status
        document.getElementById('loading').style.display = 'block';
        document.getElementById('status-message').style.display = 'none';
        
        const formData = new FormData(this);
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            }
        })
        .then(response => {
            // Oculta o carregamento
            document.getElementById('loading').style.display = 'none';
            
            if (response.ok) {
                // Exibe a mensagem de sucesso
                document.getElementById('status-message').textContent = 'Mensagem enviada com sucesso!';
                document.getElementById('status-message').className = 'status-message success';
            } else if (response.status === 400) {
                // Exibe a mensagem de erro
                document.getElementById('status-message').textContent = 'Ocorreu um erro ao enviar a mensagem. Tente novamente';
                document.getElementById('status-message').className = 'status-message error';
            }
            document.getElementById('status-message').style.display = 'block';
        })
        .catch(error => {
            // Oculta o carregamento
            document.getElementById('loading').style.display = 'none';
            
            // Exibe a mensagem de erro
            document.getElementById('status-message').textContent = 'Ocorreu um erro inesperado.';
            document.getElementById('status-message').className = 'status-message error';
            document.getElementById('status-message').style.display = 'block';
        });
    });
});
