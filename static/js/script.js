let tarefaIdParaRemover = null;
const modal = document.getElementById("modal");

function mostrarModal() {
    modal.style.display = "flex";
}

function esconderModal() {
    modal.style.display = "none";
    tarefaIdParaRemover = null;
}

function confirmarRemocao(id) {
    tarefaIdParaRemover = id;
    mostrarModal();
}

function concluirTarefa(id) {
    fetch(`/concluir/${id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "success") {
                const taskItem = document.querySelector(`li[data-id="${id}"]`);
                if (data.concluida) {
                    taskItem.classList.add("concluida");
                } else {
                    taskItem.classList.remove("concluida");
                }
            }
        })
        .catch((error) => console.error("Erro ao concluir tarefa:", error));
}

function removerTarefa(id) {
    fetch(`/remover/${id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "success") {
                const taskItem = document.querySelector(`li[data-id="${id}"]`);
                taskItem.remove();
                esconderModal();
            }
        })
        .catch((error) => {
            console.error("Erro ao remover tarefa:", error);
            esconderModal();
        });
}

document.getElementById("confirmar-remocao").addEventListener("click", () => {
    if (tarefaIdParaRemover) {
        removerTarefa(tarefaIdParaRemover);
    }
});

document
    .getElementById("cancelar-remocao")
    .addEventListener("click", esconderModal);

// Fechar modal ao clicar fora dele
window.addEventListener("click", (event) => {
    if (event.target === modal) {
        esconderModal();
    }
});

// Prevenir envio do formulário se o campo estiver vazio
document
    .getElementById("adicionar-form")
    .addEventListener("submit", function (e) {
        const input = this.querySelector('input[name="tarefa"]');
        if (!input.value.trim()) {
            e.preventDefault();
            alert("Por favor, insira um nome para a tarefa");
        }
    });
