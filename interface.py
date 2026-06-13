import customtkinter as ctk

class InterfaceReparos(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da Janela Principal
        self.title("Sistema de Gestão de Reparos")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # BANCO DE DADOS SIMULADO DE USUÁRIOS
        self.banco_usuarios = {
            "imobiliaria": "Imobiliaria",
            "inquilino": "Inquilino",
            "proprietario": "Proprietario",
            "prestador": "Prestador de Serviço"
        }

        # BANCO DE DADOS SIMULADO
        self.chamados_falsos = [
            {"id": "1", "titulo": "Infiltração grave na laje", "categoria": "Estrutural", "status": "Aguardando Aprovação", "destino": "Proprietario"},
            {"id": "2", "titulo": "Troca de fechadura da sala", "categoria": "Uso e Manutenção", "status": "Aberto", "destino": "Imobiliaria"},
            {"id": "3", "titulo": "Reparo na fiação elétrica", "categoria": "Estrutural", "status": "Em Execução", "destino": "Prestador de Serviço"}
        ]

        # Inicia mostrando a tela de login
        self.mostrar_tela_login()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    # TELA 1: LOGIN


    def mostrar_tela_login(self):
        self.limpar_tela()

        frame_login = ctk.CTkFrame(self, width=450, height=450)
        frame_login.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame_login, text="Acesso ao Sistema", font=("Arial", 22, "bold")).pack(pady=(30, 20))

        self.entry_email = ctk.CTkEntry(frame_login, placeholder_text="Digite seu Usuário ou E-mail", width=280)
        self.entry_email.pack(pady=10)

        self.entry_senha = ctk.CTkEntry(frame_login, placeholder_text="Senha", show="*", width=280)
        self.entry_senha.pack(pady=10)

        ctk.CTkButton(frame_login, text="Entrar", width=280, font=("Arial", 14, "bold"), command=self.fazer_login).pack(pady=(20, 10))
        
        self.label_erro = ctk.CTkLabel(frame_login, text="", text_color="red")
        self.label_erro.pack(pady=5)
        
        ctk.CTkLabel(frame_login, text="Testes rápidos: imobiliaria | inquilino | proprietario | prestador", text_color="gray", font=("Arial", 10)).pack(pady=5)

    def fazer_login(self):
        usuario = self.entry_email.get().lower().strip()
        
        # verifica o usuário no banco simulado e direciona para o painel correspondente
        if usuario in self.banco_usuarios:
            perfil = self.banco_usuarios[usuario]
            if perfil == "Imobiliaria":
                self.mostrar_painel_imobiliaria()
            elif perfil == "Inquilino":
                self.mostrar_painel_inquilino()
            elif perfil == "Proprietario":
                self.mostrar_painel_proprietario()
            elif perfil == "Prestador de Serviço":
                self.mostrar_painel_prestador()
        elif usuario == "":
            self.label_erro.configure(text="Preencha o usuário!")
        else:
            self.label_erro.configure(text="Usuário não encontrado!")

  
    # TELA 2: PAINEL DA IMOBILIÁRIA (ADMIN)

    def mostrar_painel_imobiliaria(self):
        self.limpar_tela()

        frame_painel = ctk.CTkFrame(self)
        frame_painel.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_painel, text="Painel Administrativo - Imobiliária", font=("Arial", 24, "bold")).pack(pady=20, anchor="w", padx=20)

        ctk.CTkButton(frame_painel, text="👥 Cadastrar Novo Usuário", height=40, width=350, command=self.mostrar_tela_cadastro).pack(pady=10, padx=20, anchor="w")
        ctk.CTkButton(frame_painel, text="📋 Ver Todos os Chamados da Agência", height=40, width=350, command=self.mostrar_tela_ver_chamados_imob).pack(pady=10, padx=20, anchor="w")

        ctk.CTkButton(frame_painel, text="Sair", fg_color="red", hover_color="darkred", width=100, command=self.mostrar_tela_login).place(relx=0.95, rely=0.95, anchor="se")

    def mostrar_tela_ver_chamados_imob(self):
        self.limpar_tela()
        frame_listagem = ctk.CTkFrame(self)
        frame_listagem.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_listagem, text="Todos os Chamados do Sistema", font=("Arial", 24, "bold")).pack(pady=20, anchor="w", padx=20)

        scroll_chamados = ctk.CTkScrollableFrame(frame_listagem, width=700, height=350)
        scroll_chamados.pack(pady=10, padx=20, fill="both", expand=True)

        for chamado in self.chamados_falsos:
            card = ctk.CTkFrame(scroll_chamados, fg_color="#2b2b2b")
            card.pack(fill="x", pady=5, padx=5)
            texto = f"ID: {chamado['id']} | {chamado['titulo']}\nCategoria: {chamado['categoria']} | Atual: {chamado['destino']} | Status: {chamado['status']}"
            ctk.CTkLabel(card, text=texto, justify="left", font=("Arial", 13)).pack(side="left", padx=15, pady=10)
            ctk.CTkButton(card, text="Editar Status", width=100).pack(side="right", padx=15, pady=10)

        ctk.CTkButton(frame_listagem, text="Voltar", fg_color="gray", command=self.mostrar_painel_imobiliaria).pack(pady=15)

    def mostrar_tela_cadastro(self):
        self.limpar_tela()
        frame_cadastro = ctk.CTkFrame(self)
        frame_cadastro.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_cadastro, text="Cadastrar Novo Acesso", font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkEntry(frame_cadastro, placeholder_text="Nome Completo", width=350).pack(pady=10)
        ctk.CTkEntry(frame_cadastro, placeholder_text="Usuário", width=350).pack(pady=10)
        ctk.CTkEntry(frame_cadastro, placeholder_text="Senha provisória", show="*", width=350).pack(pady=10)
        ctk.CTkOptionMenu(frame_cadastro, values=["Inquilino", "Proprietario", "Prestador de Serviço"], width=350).pack(pady=10)

        ctk.CTkButton(frame_cadastro, text="Salvar Cadastro", width=350, fg_color="green").pack(pady=20)
        ctk.CTkButton(frame_cadastro, text="Voltar", width=350, fg_color="gray", command=self.mostrar_painel_imobiliaria).pack(pady=5)

  
    # TELA 3: PAINEL DO INQUILINO

    def mostrar_painel_inquilino(self):
        self.limpar_tela()
        frame_painel = ctk.CTkFrame(self)
        frame_painel.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_painel, text="Área do Inquilino", font=("Arial", 24, "bold")).pack(pady=20, anchor="w", padx=20)

        ctk.CTkButton(frame_painel, text="🛠️ Abrir Novo Chamado de Manutenção", height=40, width=300).pack(pady=10, padx=20, anchor="w")
        ctk.CTkButton(frame_painel, text="🔍 Acompanhar Meus Chamados", height=40, width=300).pack(pady=10, padx=20, anchor="w")

        ctk.CTkButton(frame_painel, text="Sair", fg_color="red", hover_color="darkred", width=100, command=self.mostrar_tela_login).place(relx=0.95, rely=0.95, anchor="se")


    # TELA 4: PAINEL DO PROPRIETÁRIO
   
    def mostrar_painel_proprietario(self):
        self.limpar_tela()
        frame_painel = ctk.CTkFrame(self)
        frame_painel.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_painel, text="Área do Proprietário", font=("Arial", 24, "bold")).pack(pady=20, anchor="w", padx=20)
        ctk.CTkLabel(frame_painel, text="⚠️ Problemas estruturais pendentes da sua aprovação:", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(0, 10))

        scroll_chamados = ctk.CTkScrollableFrame(frame_painel, width=700, height=300)
        scroll_chamados.pack(pady=10, padx=20, fill="both", expand=True)

        # Filtra e mostra só os chamados q sao proproprietario
        for chamado in self.chamados_falsos:
            if chamado["destino"] == "Proprietario":
                card = ctk.CTkFrame(scroll_chamados, fg_color="#4a3b1c")
                card.pack(fill="x", pady=5, padx=5)
                texto = f"ID: {chamado['id']} | {chamado['titulo']}\nStatus: {chamado['status']}"
                ctk.CTkLabel(card, text=texto, justify="left", font=("Arial", 13)).pack(side="left", padx=15, pady=10)
                
                ctk.CTkButton(card, text="Aprovar Reparo", width=120, fg_color="green", hover_color="darkgreen").pack(side="right", padx=15, pady=10)

        ctk.CTkButton(frame_painel, text="Sair", fg_color="red", hover_color="darkred", width=100, command=self.mostrar_tela_login).place(relx=0.95, rely=0.95, anchor="se")


    # TELA 5: PAINEL DO PRESTADOR DE SERVIÇO
  
    def mostrar_painel_prestador(self):
        self.limpar_tela()
        frame_painel = ctk.CTkFrame(self)
        frame_painel.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_painel, text="Área do Prestador de Serviços", font=("Arial", 24, "bold")).pack(pady=20, anchor="w", padx=20)
        ctk.CTkLabel(frame_painel, text="🛠️ Serviços atribuídos a você para execução:", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(0, 10))

        scroll_chamados = ctk.CTkScrollableFrame(frame_painel, width=700, height=300)
        scroll_chamados.pack(pady=10, padx=20, fill="both", expand=True)

        # Filtra e mostra só os chamados que estão para o prestador
        for chamado in self.chamados_falsos:
            if chamado["destino"] == "Prestador de Serviço":
                card = ctk.CTkFrame(scroll_chamados, fg_color="#1c3a4a") # Cor diferenciada
                card.pack(fill="x", pady=5, padx=5)
                texto = f"ID: {chamado['id']} | {chamado['titulo']}\nStatus: {chamado['status']}"
                ctk.CTkLabel(card, text=texto, justify="left", font=("Arial", 13)).pack(side="left", padx=15, pady=10)
                
                ctk.CTkButton(card, text="Marcar como Concluído", width=160, fg_color="#1f538d").pack(side="right", padx=15, pady=10)

        ctk.CTkButton(frame_painel, text="Sair", fg_color="red", hover_color="darkred", width=100, command=self.mostrar_tela_login).place(relx=0.95, rely=0.95, anchor="se")


if __name__ == "__main__":
    app = InterfaceReparos()
    app.mainloop()