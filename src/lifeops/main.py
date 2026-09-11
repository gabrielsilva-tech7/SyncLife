from banco import (
    criar_tabelas,
    adicionar_tarefa,
    listar_tarefas,
    concluir_tarefa,
    excluir_tarefa,
    adicionar_compromisso,
    listar_compromissos,
    excluir_compromisso,
    adicionar_gasto,
    listar_gastos,
    excluir_gasto
)


def menu_tarefas():
    while True:
        print("\n===== Tarefas =====")
        print("1 - Listar tarefas")
        print("2 - Adicionar tarefa")
        print("3 - Concluir tarefa")
        print("4 - Excluir tarefa")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break

        elif opcao == "1":
            tarefas = listar_tarefas()

            if len(tarefas) == 0:
                print("Nenhuma tarefa cadastrada!")
            else:
                for tarefa in tarefas:
                    status = "[✓]" if tarefa[2] == 1 else "[ ]"
                    print(f"{tarefa[0]} - {status} {tarefa[1]}")

        elif opcao == "2":
            tarefa = input("Digite a tarefa: ")
            adicionar_tarefa(tarefa)
            print("Tarefa adicionada!")


        elif opcao == "3":
            try:
                id_tarefa = int(input("Digite o ID da tarefa concluída: "))
            except ValueError:
                print("ID Invalido!")
                continue

            if concluir_tarefa(id_tarefa):
                print("Tarefa concluída!")
            else:
                print("Tarefa não encontrada")


        elif opcao == "4":
            try:
                id_tarefa = int(input("Digite o ID da tarefa que deseja excluir: "))
            except ValueError:
                print("ID invalido!")
                continue
            if excluir_tarefa(id_tarefa):
                print("Tarefa excluída!")
            else:
                print("Tarefa não encontrada!")


        else:
            print("Opção inválida!")

def menu_compromissos():
    while True:
        print("\n===== Compromissos =====")
        print("1 - Listar compromissos")
        print("2 - Adicionar compromisso")
        print("3 - Excluir compromisso")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break
        

        elif opcao == "1":
            compromissos = listar_compromissos()

            if len(compromissos) == 0:
                print("Nenhum compromisso cadastrado.")
            else:
                for compromisso in compromissos:
                    print(f"{compromisso[0]} - {compromisso[1]}")

        elif opcao == "2":
            descricao = input("Digite um compromisso: ")
            adicionar_compromisso(descricao)
            print("Compromisso cadastrado!")

        elif opcao == "3":
            try:
                id_compromisso = int(
                input("Digite o ID do compromisso que deseja excluir: ")
                )
            except ValueError:
                print("ID Invalido!")
                continue

            if excluir_compromisso(id_compromisso):
                print("Compromisso excluído!")

            else:
                print("Compromissso não encontrado.")


def menu_gastos():
    while True:
        print("\n===== Gastos =====")
        print("1 - Listar gastos")
        print("2 - Adicionar gasto")
        print("3 - Ver total")
        print("4 - Excluir gasto")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break

        elif opcao == "1":
            gastos = listar_gastos()
            print("\n===== Lista de gastos =====")

            if len(gastos) == 0:
                print("Nenhum gasto cadastrado!")
            else:
                for gasto in gastos:
                    print(f"{gasto[0]} - {gasto[1]} R$ {gasto[2]:.2f}")

        elif opcao == "2":
            nome = input("Digite o nome do gasto: ")
            try:
                valor = float(input("Digite o valor do gasto: R$ "))
            except ValueError:
                print("Valor inválido!")
                continue

            adicionar_gasto(nome, valor)

            print("Gasto adicionado!")


        elif opcao == "3":
            gastos = listar_gastos()
            total = 0

            for gasto in gastos:
                total += gasto[2]

            print(f"\nTotal gasto: R$ {total:.2f}")

        elif opcao == "4":
            try:
                id_gasto = int(
                input("Digite o ID do gasto que deseja excluir: ")
                )
            except ValueError:
                print("ID Invalido!")
                continue

            if excluir_gasto(id_gasto):
                print("Gasto excluído!")
            else:
                print("Gasto não encontrado!")

def mostrar_resumo():
    tarefas = listar_tarefas()
    compromissos = listar_compromissos()
    gastos = listar_gastos()

    pendentes = 0
    concluidas = 0

    for tarefa in tarefas:
        if tarefa[2] == 1:
            concluidas += 1
        else:
            pendentes += 1

    total_gastos = 0

    for gasto in gastos:
        total_gastos += gasto[2]

    print("\n===== Resumo =====")
    print(f"Tarefas pendentes: {pendentes}")
    print(f"Tarefas concluídas: {concluidas}")
    print(f"Compromissos: {len(compromissos)}")
    print(f"Total gasto: R$ {total_gastos:.2f}") 



def main():

    criar_tabelas()

    while True:

        print("\n==== LifeOps ====")
        print("1 - Tarefas")
        print("2 - Compromissos")
        print("3 - Gastos")
        print("4 - Resumo")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_tarefas()
            

        elif opcao == "2":
            menu_compromissos()

        elif opcao == "3":
            menu_gastos()

        elif opcao == "4":
            mostrar_resumo()

        elif opcao == "0":
            print("Saindo do LifeOPS...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()