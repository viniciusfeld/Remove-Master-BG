document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('drop-zone');
    const dragMessage = document.querySelector('.drag-message');
    const defaultText = document.querySelector('.default-text');
    const fileInput = document.getElementById('file');
    const fileNameDisplay = document.getElementById('file-name');
    const removeFileButton = document.getElementById('remove-file');
    const fileInfo = document.getElementById('file-info');
    const errorMessageElement = document.getElementById('error-message');
    const uploadButton = document.getElementById('upload-button');
    // const loadingElement = document.getElementById('loading'); // Elemento de loading
    const allowedFileTypes = ['image/jpeg', 'image/png', 'image/gif'];

    // Função para obter o token CSRF
    function getCsrfToken() {
        const tokenElement = document.querySelector('meta[name="csrf-token"]');
        return tokenElement ? tokenElement.content : '';
    }

    function showLoadingOverlay() {
        document.getElementById('loading-overlay').classList.remove('hidden');
        simulateStatusUpdates(); // Função para simular atualizações de status
        toggleUploadButton(false);
    }
    
    // Ocultar o overlay
    function hideLoadingOverlay() {
        document.getElementById('loading-overlay').classList.add('hidden');

        toggleUploadButton(true); // Habilita o botão de enviar
    }
    
    // Simulação de atualizações de status
    function simulateStatusUpdates() {
        const statusMessages = [
            'Recebendo imagem...',
            'Removendo fundo...',
            'Refinando imagem...',
            'Inserindo fundo branco',
            'Finalizando...'
        ];
    
        let index = 0;
        const statusElement = document.getElementById('status-update');
        
        const interval = setInterval(() => {
            index++;
            if (index >= statusMessages.length) {
                index = 0;
            }
            statusElement.textContent = statusMessages[index];
        }, 2000); // Atualiza a cada 2 segundos
    
        // Parar simulação após o processamento
        setTimeout(() => {
            clearInterval(interval);
            statusElement.textContent = 'Pronto!';
        }, 10000); // Simula o processamento por 10 segundos
    }
    
    // Função para exibir a mensagem de erro
    function showError(message) {
        if (errorMessageElement) {
            errorMessageElement.textContent = message;
            errorMessageElement.style.display = 'block'; // Mostra a mensagem de erro
        } else {
            console.error("Elemento de mensagem de erro não encontrado.");
        }
    }

    // Função para limpar a mensagem de erro
    function clearError() {
        if (errorMessageElement) {
            errorMessageElement.textContent = '';
            errorMessageElement.style.display = 'none'; // Oculta a mensagem de erro
        }
    }

    // Função para habilitar ou desabilitar o botão de enviar
    function toggleUploadButton(enabled) {
        if (uploadButton) {
            if (enabled) {
                uploadButton.classList.remove('disabled');
                uploadButton.disabled = false;
            } else {
                uploadButton.classList.add('disabled');
                uploadButton.disabled = true;
            }
        } else {
            console.error("Botão de envio não encontrado.");
        }
    }

    // Função para mostrar o loading
    // function showLoading() {
    //     if (loadingElement) {
    //         loadingElement.style.display = 'block';
    //     }
    //     toggleUploadButton(false); // Desabilita o botão de enviar
    // }

    // // Função para ocultar o loading
    // function hideLoading() {
    //     if (loadingElement) {
    //         loadingElement.style.display = 'none';
    //     }
    //     toggleUploadButton(true); // Habilita o botão de enviar
    // }

    // Função para atualizar a visibilidade do botão de remover
    function updateRemoveButtonVisibility() {
        if (fileInput.files.length > 0) {
            removeFileButton.style.display = 'inline'; // Mostrar o botão se um arquivo estiver presente
        } else {
            removeFileButton.style.display = 'none'; // Ocultar o botão se nenhum arquivo estiver presente
        }
    }

    // Função para atualizar a exibição do nome do arquivo
    function updateFileDisplay() {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            if (validateFile(file)) {
                fileNameDisplay.textContent = file.name;
                fileNameDisplay.title = file.name; // Exibe o nome completo ao passar o mouse
                defaultText.style.display = 'none'; // Oculta a mensagem padrão
                dropZone.style.backgroundColor = ''; // Remove o fundo da drop zone
                clearError(); // Limpa a mensagem de erro
                toggleUploadButton(true); // Habilita o botão de enviar
            } else {
                fileInput.value = ''; // Limpa o input de arquivo se o arquivo não for válido
                fileInput.files = new DataTransfer().files; // Limpa os arquivos do input
                updateFileDisplay(); // Atualiza a exibição do arquivo
                toggleUploadButton(false); // Desabilita o botão de enviar
            }
        } else {
            fileNameDisplay.textContent = 'Nenhuma imagem selecionada';
            fileNameDisplay.title = ''; // Limpa o título
            defaultText.style.display = 'block'; // Mostra a mensagem padrão
            toggleUploadButton(false); // Desabilita o botão de enviar
        }
        updateRemoveButtonVisibility(); // Atualiza a visibilidade do botão de remover
    }

    // Função para validar o arquivo
    function validateFile(file) {
        if (!allowedFileTypes.includes(file.type)) {
            showError('Tipo de arquivo não suportado. Por favor, envie uma imagem.');
            return false;
        }
        return true;
    }

    // Função para lidar com a seleção de arquivos
    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (validateFile(file)) {
                fileInput.files = files; // Para que o input de arquivo contenha o arquivo
                updateFileDisplay(); // Atualiza a exibição do arquivo
            } else {
                fileInput.value = ''; // Limpa o input de arquivo se o arquivo não for válido
                fileInput.files = new DataTransfer().files; // Limpa os arquivos do input
                updateFileDisplay(); // Atualiza a exibição do arquivo
            }
        }
    }

    // Inicializa o botão de envio como desativado
    toggleUploadButton(false);

    dropZone.addEventListener('dragenter', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dragMessage.style.display = 'block';
        defaultText.style.opacity = '0';
        fileInfo.style.opacity = '0'; // Oculta o texto "Nenhuma imagem selecionada"
        clearError(); // Limpa a mensagem de erro
    });

    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        if (!dropZone.contains(e.relatedTarget)) {
            dragMessage.style.display = 'none';
            defaultText.style.opacity = fileInput.files.length > 0 ? '0' : '1'; // Mostra ou oculta a mensagem padrão
            fileInfo.style.opacity = '1'; // Mostra o texto "Nenhuma imagem selecionada"
        }
    });

    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dragMessage.style.display = 'block';
        defaultText.style.opacity = '0';
        fileInfo.style.opacity = '0'; // Oculta o texto "Nenhuma imagem selecionada"
        dropZone.style.backgroundColor = '#f0f0f0'; // Alterar o fundo quando o arquivo está sendo arrastado
        clearError(); // Limpa a mensagem de erro
    });

    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dragMessage.style.display = 'none';
        defaultText.style.opacity = '0'; // Oculta a mensagem padrão ao soltar o arquivo
        fileInfo.style.opacity = '1'; // Mostra o texto "Nenhuma imagem selecionada"
        dropZone.style.backgroundColor = ''; // Remove o fundo quando o arquivo é solto
        clearError(); // Limpa a mensagem de erro

        // Lidar com o arquivo
        handleFiles(e.dataTransfer.files);
    });

    removeFileButton.addEventListener('click', function(e) {
        e.stopPropagation(); // Evita que o clique no botão de remover acione o clique na drop zone
        fileInput.value = ''; // Limpa o input de arquivo
        fileInput.files = new DataTransfer().files; // Limpa os arquivos do input
        updateFileDisplay(); // Atualiza a exibição do arquivo
        dropZone.style.backgroundColor = ''; // Remove o fundo da drop zone após a remoção
    });

    dropZone.addEventListener('click', function() {
        if (fileInput.files.length === 0) {
            fileInput.click(); // Abre o seletor de arquivos apenas se nenhum arquivo estiver presente
        }
    });

    fileInput.addEventListener('change', function() {
        handleFiles(fileInput.files); // Lida com a seleção de arquivos
    });

    // Atualiza a mensagem padrão quando o arquivo é removido
    fileInput.addEventListener('input', function() {
        updateFileDisplay(); // Atualiza a exibição do arquivo ao alterar o input
    });

    // Função para enviar o arquivo
    function sendFile() {
        const file = fileInput.files[0];
        if (!file) {
            console.error('Nenhum arquivo selecionado.');
            return;
        }
    
        showLoadingOverlay(); // Mostra o loading
    
        const formData = new FormData();
        formData.append('file', file);
    
        fetch('/upload/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => {
            hideLoadingOverlay(); // Oculta o loading
            if (response.ok) {
                return response.json(); // Converte a resposta para JSON
            } else {
                throw new Error('Erro na requisição');
            }
        })
        .then(data => {
            console.log('Arquivo enviado com sucesso:', data);
            if (data.redirect_url) {
                window.location.href = data.redirect_url; // Redireciona o usuário
            } else {
                showError('Erro no processamento. Tente novamente.'); // Mensagem de erro genérica
            }
        })
        .catch(error => {
            hideLoadingOverlay(); // Oculta o loading em caso de erro
            console.error('Erro:', error);
            showError('Falha ao enviar o arquivo. Por favor, tente novamente.'); // Mostra a mensagem de erro
        });
    }
    

    // Adiciona o listener de clique para o botão de envio
    uploadButton.addEventListener('click', sendFile);
});

document.getElementById("upload-title").addEventListener("click", function() {
    document.getElementById("file").click(); // Simula o clique no input file
});
