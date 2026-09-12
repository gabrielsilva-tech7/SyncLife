const API = "";


// =========================
// UTILIDADES
// =========================

function abrirModal(id) {
    document.getElementById(id).classList.add("aberto");
}


function fecharModal(id) {
    document.getElementById(id).classList.remove("aberto");
}


function mostrarToast(mensagem, erro = false) {
    const toast = document.getElementById("toast");

    toast.textContent = mensagem;

    toast.classList.toggle("erro", erro);
    toast.classList.add("mostrar");

    setTimeout(() => {
        toast.classList.remove("mostrar");
    }, 2500);
}


function formatarDinheiro(valor) {
    return Number(valor).toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}


async function requisicao(url, opcoes = {}) {
    const resposta = await fetch(API + url, opcoes);

    if (!resposta.ok) {
        throw new Error("Erro na comunicação com o servidor.");
    }

    return resposta.json();
}


// =========================
// RESUMO
// =========================

async function carregarResumo() {

    try {

        const resumo = await requisicao("/resumo");

        document.getElementById("tarefas-pendentes").textContent =
            resumo.tarefas_pendentes;

        document.getElementById("tarefas-concluidas").textContent =
            resumo.tarefas_concluidas;

        document.getElementById("total-compromissos").textContent =
            resumo.compromissos;

        document.getElementById("total-gastos").textContent =
            formatarDinheiro(resumo.total_gastos);

    } catch (erro) {

        console.error(erro);

    }

}


// =========================
// TAREFAS
// =========================

async function carregarTarefas() {

    const lista = document.getElementById("lista-tarefas");

    try {

        const tarefas = await requisicao("/tarefas");

        lista.innerHTML = "";

        if (tarefas.length === 0) {

            lista.innerHTML =
                `<div class="vazio">Nenhuma tarefa cadastrada.</div>`;

            return;
        }

        tarefas.forEach(tarefa => {

            const item = document.createElement("div");

            item.className =
                `item ${tarefa.concluida ? "concluida" : ""}`;

            item.innerHTML = `
                <div class="item-info">

                    <button
                        class="check ${tarefa.concluida ? "ativo" : ""}"
                        ${tarefa.concluida ? "disabled" : ""}
                        onclick="concluirTarefa(${tarefa.id})">
                    </button>

                    <span class="item-texto">
                        ${escaparHTML(tarefa.descricao)}
                    </span>

                </div>

                <div class="item-acoes">

                    <button
                        class="excluir"
                        title="Excluir tarefa"
                        onclick="excluirTarefa(${tarefa.id})">
                        ×
                    </button>

                </div>
            `;

            lista.appendChild(item);

        });

    } catch (erro) {

        lista.innerHTML =
            `<div class="vazio">Não foi possível carregar as tarefas.</div>`;

    }

}


async function salvarTarefa() {

    const input = document.getElementById("descricao-tarefa");

    const descricao = input.value.trim();

    if (!descricao) {

        mostrarToast("Digite uma tarefa.", true);
        input.focus();

        return;
    }

    try {

        await requisicao("/tarefas", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                descricao
            })
        });

        input.value = "";

        fecharModal("modal-tarefa");

        mostrarToast("Tarefa adicionada.");

        await atualizarTudo();

    } catch (erro) {

        mostrarToast("Não foi possível adicionar a tarefa.", true);

    }

}


async function concluirTarefa(id) {

    try {

        await requisicao(`/tarefas/${id}/concluir`, {
            method: "PATCH"
        });

        mostrarToast("Tarefa concluída.");

        await atualizarTudo();

    } catch (erro) {

        mostrarToast("Não foi possível concluir a tarefa.", true);

    }

}


async function excluirTarefa(id) {

    const confirmar =
        confirm("Deseja realmente excluir esta tarefa?");

    if (!confirmar) return;

    try {

        await requisicao(`/tarefas/${id}`, {
            method: "DELETE"
        });

        mostrarToast("Tarefa excluída.");

        await atualizarTudo();

    } catch (erro) {

        mostrarToast("Não foi possível excluir a tarefa.", true);

    }

}


// =========================
// COMPROMISSOS
// =========================

async function carregarCompromissos() {

    const lista =
        document.getElementById("lista-compromissos");

    try {

        const compromissos =
            await requisicao("/compromissos");

        lista.innerHTML = "";

        if (compromissos.length === 0) {

            lista.innerHTML =
                `<div class="vazio">Nenhum compromisso cadastrado.</div>`;

            return;
        }

        compromissos.forEach(compromisso => {

            const item = document.createElement("div");

            item.className = "item";

            item.innerHTML = `
                <div class="item-info">

                    <span>•</span>

                    <span class="item-texto">
                        ${escaparHTML(compromisso.descricao)}
                    </span>

                </div>

                <button
                    class="excluir"
                    title="Excluir compromisso"
                    onclick="excluirCompromisso(${compromisso.id})">
                    ×
                </button>
            `;

            lista.appendChild(item);

        });

    } catch (erro) {

        lista.innerHTML =
            `<div class="vazio">Não foi possível carregar os compromissos.</div>`;

    }

}


async function salvarCompromisso() {

    const input =
        document.getElementById("descricao-compromisso");

    const descricao = input.value.trim();

    if (!descricao) {

        mostrarToast("Digite um compromisso.", true);
        input.focus();

        return;
    }

    try {

        await requisicao("/compromissos", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                descricao
            })

        });

        input.value = "";

        fecharModal("modal-compromisso");

        mostrarToast("Compromisso adicionado.");

        await atualizarTudo();

    } catch (erro) {

        mostrarToast(
            "Não foi possível adicionar o compromisso.",
            true
        );

    }

}


async function excluirCompromisso(id) {

    if (!confirm("Deseja excluir este compromisso?")) {
        return;
    }

    try {

        await requisicao(`/compromissos/${id}`, {
            method: "DELETE"
        });

        mostrarToast("Compromisso excluído.");

        await atualizarTudo();

    } catch (erro) {

        mostrarToast(
            "Não foi possível excluir o compromisso.",
            true
        );

    }

}


// =========================
// GASTOS
// =========================

async function carregarGastos() {

    const lista =
        document.getElementById("lista-gastos");

    try {

        const gastos = await requisicao("/gastos");

        lista.innerHTML = "";

        if (gastos.length === 0) {

            lista.innerHTML =
                `<div class="vazio">Nenhum gasto registrado.</div>`;

            return;
        }

        gastos.forEach(gasto => {

            const item = document.createElement("div");

            item.className = "item";

            item.innerHTML = `
                <div class="item-info">

                    <span>•</span>

                    <span class="item-texto">
                        ${escaparHTML(gasto.nome)}
                    </span>

                </div>

                <div class="item-acoes">

                    <span class="valor">
                        ${formatarDinheiro(gasto.valor)}
                    </span>

                    <button
                        class="excluir"
                        title="Excluir gasto"
                        onclick="excluirGasto(${gasto.id})">
                        ×
                    </button>

                </div>
            `;

            lista.appendChild(item);

        });

    } catch (erro) {

        lista.innerHTML =
            `<div class="vazio">Não foi possível carregar os gastos.</div>`;

    }

}


async function salvarGasto() {

    const nomeInput =
        document.getElementById("nome-gasto");

    const valorInput =
        document.getElementById("valor-gasto");

    const nome = nomeInput.value.trim();

    const valor = Number(valorInput.value);

    if (!nome) {

        mostrarToast("Digite o nome do gasto.", true);
        nomeInput.focus();

        return;
    }

    if (!valor || valor <= 0) {

        mostrarToast("Digite um valor válido.", true);
        valorInput.focus();

        return;
    }

    try {

        await requisicao("/gastos", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                nome,
                valor
            })

        });

        nomeInput.value = "";
        valorInput.value = "";

        fecharModal("modal-gasto");

        mostrarToast("Gasto registrado.");

        await atualizarTudo();

    } catch (erro) {

        mostrarToast(
            "Não foi possível registrar o gasto.",
            true
        );

    }

}


async function excluirGasto(id) {

    if (!confirm("Deseja excluir este gasto?")) {
        return;
    }

    try {

        await requisicao(`/gastos/${id}`, {
            method: "DELETE"
        });

        mostrarToast("Gasto excluído.");

        await atualizarTudo();

    } catch (erro) {

        mostrarToast(
            "Não foi possível excluir o gasto.",
            true
        );

    }

}


// =========================
// SEGURANÇA DO HTML
// =========================

function escaparHTML(texto) {

    const elemento = document.createElement("div");

    elemento.textContent = texto;

    return elemento.innerHTML;

}


// =========================
// ATUALIZAÇÃO GERAL
// =========================

async function atualizarTudo() {

    await Promise.all([
        carregarResumo(),
        carregarTarefas(),
        carregarCompromissos(),
        carregarGastos()
    ]);

}


// fechar modal clicando no fundo

document.querySelectorAll(".modal").forEach(modal => {

    modal.addEventListener("click", evento => {

        if (evento.target === modal) {
            fecharModal(modal.id);
        }

    });

});


// ESC fecha os modais

document.addEventListener("keydown", evento => {

    if (evento.key === "Escape") {

        document.querySelectorAll(".modal.aberto")
            .forEach(modal => fecharModal(modal.id));

    }

});


// ENTER envia formulários

document.getElementById("descricao-tarefa")
    .addEventListener("keydown", evento => {

        if (evento.key === "Enter") {
            salvarTarefa();
        }

    });


document.getElementById("descricao-compromisso")
    .addEventListener("keydown", evento => {

        if (evento.key === "Enter") {
            salvarCompromisso();
        }

    });


document.getElementById("valor-gasto")
    .addEventListener("keydown", evento => {

        if (evento.key === "Enter") {
            salvarGasto();
        }

    });


// inicia o Sync

atualizarTudo();