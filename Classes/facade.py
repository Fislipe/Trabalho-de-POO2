from Classes.usuarios import UsuarioFactory
from Classes.chamado import Chamado
from supabase import create_client, Client
from datetime import datetime

SUPABASE_URL = "https://aawotiynbpxgykxzlyux.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFhd290aXluYnB4Z3lreHpseXV4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE2NDAzMzAsImV4cCI6MjA5NzIxNjMzMH0.ntk2VmlVvUHphWyZCMXx1_Ng5jaVPCuy0yUQmvwpshY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SistemaImobiliarioFacade:
    @staticmethod
    def registrar_novo_usuario(perfil, nome, documento, email, senha):
        try:
            novo_usuario = UsuarioFactory.criar_usuario(perfil, nome, documento, email, senha)
            
            dados = {
                "nome": nome,
                "email": email,
                "senha": senha,
                "perfil": novo_usuario.obter_perfil(),
                "documento": documento
            }
            supabase.table("usuarios").insert(dados).execute()
            
            return novo_usuario
        except Exception as e:
            raise ValueError(f"Erro no cadastro: {str(e)}")

    @staticmethod
    def autenticar_usuario(email, senha_digitada):
        resposta = supabase.table("usuarios").select("*").eq("email", email).execute()
        usuarios_encontrados = resposta.data if hasattr(resposta, 'data') else resposta.get('data', []) 
        
        if usuarios_encontrados:
            dados_db = usuarios_encontrados[0]
            
            usuario_obj = UsuarioFactory.criar_usuario(
                perfil=dados_db['perfil'],
                nome=dados_db['nome'],
                documento=dados_db.get('documento', dados_db['email']),
                email=dados_db['email'],
                senha=dados_db['senha']
            )
            
            if usuario_obj.validar_senha(senha_digitada):
                return usuario_obj
                
        return None

    @staticmethod
    def abrir_novo_chamado(titulo, descricao, categoria, criado_por=None):
        novo_chamado = Chamado(titulo, descricao, categoria)

        # Agora grava também a data de abertura formatada no momento do insert
        dados = {
            "id": novo_chamado.id,
            "titulo": novo_chamado.titulo,
            "descricao": novo_chamado.descricao,
            "categoria": novo_chamado.categoria,
            "status": novo_chamado.get_status(),
            "responsavel": novo_chamado.responsavel,
            "criado_por": criado_por,
            "data_abertura": datetime.now().strftime('%d/%m/%Y %H:%M')
        }
        supabase.table("chamados").insert(dados).execute()
        
        supabase.table("historico_chamados").insert({
            "chamado_id": novo_chamado.id,
            "mensagem": novo_chamado.historico[-1],
            "data_hora": datetime.now().isoformat()
        }).execute()
        
        return novo_chamado
        
    @staticmethod
    def atualizar_andamento_chamado(chamado, prestador_email=None):
        chamado.avancar_status()

        dados_update = {
            "status": chamado.get_status()
        }
        if prestador_email:
            dados_update["prestador"] = prestador_email

        if chamado.get_status() == "Encerrado":
            dados_update["data_encerramento"] = datetime.now().strftime('%d/%m/%Y %H:%M')

        supabase.table("chamados").update(dados_update).eq("id", chamado.id).execute()

        supabase.table("historico_chamados").insert({
            "chamado_id": chamado.id,
            "mensagem": chamado.historico[-1],
            "data_hora": datetime.now().isoformat()
        }).execute()

        return chamado.get_status()

    @staticmethod
    def inquilino_confirmar_reparo(chamado):
        chamado.confirmar_reparo()
        
        supabase.table("historico_chamados").insert({
            "chamado_id": chamado.id,
            "mensagem": chamado.historico[-1],
            "data_hora": datetime.now().isoformat()
        }).execute()
    
    @staticmethod
    def buscar_chamados_por_usuario(email):
        resposta = supabase.table("chamados").select("*").eq("criado_por", email).execute()
        return resposta.data if hasattr(resposta, 'data') else resposta.get('data', [])
    
    @staticmethod
    def buscar_chamados_estruturais():
        # MODIFICADO: O proprietário só vê o que é estrutural E está sob a responsabilidade dele atualmente
        resposta = supabase.table("chamados").select("*").eq("categoria", "Estrutural").eq("responsavel", "Proprietário").eq("status", "Aberto").execute()
        return resposta.data if hasattr(resposta, 'data') else resposta.get('data', [])
    
    @staticmethod
    def buscar_chamados_imobiliaria():
        resposta = supabase.table("chamados").select("*").eq("responsavel", "Imobiliária").eq("status", "Aberto").execute()
        return resposta.data if hasattr(resposta, 'data') else resposta.get('data', [])
    
    @staticmethod
    def buscar_chamado_por_id(chamado_id):
        resposta = supabase.table("chamados").select("*").eq("id", chamado_id).execute()
        if not hasattr(resposta, 'data') or not resposta.data:
            return None
            
        dados = resposta.data[0]
        chamado = Chamado(dados['titulo'], dados['descricao'], dados['categoria'])
        chamado.id = dados['id']
        chamado.responsavel = dados['responsavel']
        
        chamado.definir_estado(dados['status'])
        
        resp_hist = supabase.table("historico_chamados").select("mensagem").eq("chamado_id", chamado_id).order("data_hora").execute()
        if hasattr(resp_hist, 'data') and resp_hist.data:
            chamado.historico = [h['mensagem'] for h in resp_hist.data]
            
        return chamado

    @staticmethod
    def buscar_todos_prestadores():
        resposta = supabase.table("usuarios").select("*").execute()
        usuarios = resposta.data if hasattr(resposta, 'data') else resposta.get('data', [])
        
        prestadores = []
        for u in usuarios:
            p_lower = u.get('perfil', '').lower()
            if 'prestador' in p_lower or 'serviço' in p_lower or 'servico' in p_lower:
                prestadores.append(u)
        return prestadores

    @staticmethod
    def buscar_chamados_prestador(email):
        resposta = supabase.table("chamados").select("*").eq("prestador", email).in_("status", ["Em Análise", "Em Execução"]).execute()
        return resposta.data if hasattr(resposta, 'data') else resposta.get('data', [])

    @staticmethod
    def atribuir_chamado_a_prestador(chamado, prestador_email):
        msg = f"Imobiliária atribuiu o serviço ao prestador: {prestador_email}"
        chamado.adicionar_historico(msg)
        
        supabase.table("historico_chamados").insert({
            "chamado_id": chamado.id,
            "mensagem": msg,
            "data_hora": datetime.now().isoformat()
        }).execute()
        
        SistemaImobiliarioFacade.atualizar_andamento_chamado(chamado, prestador_email=prestador_email)

    @staticmethod
    def aprovar_orcamento(chamado):
        # repassa o trabalho pra imobiliaria
        chamado.responsavel = "Imobiliária"
        msg = "Proprietário aprovou o orçamento. Chamado retornado para a Imobiliária selecionar o prestador."
        chamado.adicionar_historico(msg)
        
        # att a responsabilidade no banco de dados
        supabase.table("chamados").update({
            "responsavel": "Imobiliária"
        }).eq("id", chamado.id).execute()
        
        supabase.table("historico_chamados").insert({
            "chamado_id": chamado.id,
            "mensagem": msg,
            "data_hora": datetime.now().isoformat()
        }).execute()

    @staticmethod
    def buscar_historico_completo():
        resp_chamados = supabase.table("chamados").select("*").execute()
        chamados = resp_chamados.data if hasattr(resp_chamados, 'data') else resp_chamados.get('data', [])

        resp_usuarios = supabase.table("usuarios").select("email", "nome").execute()
        usuarios = resp_usuarios.data if hasattr(resp_usuarios, 'data') else resp_usuarios.get('data', [])
        
        mapa_nomes = {u['email']: u['nome'] for u in usuarios}

        for c in chamados:
            email_criador = c.get('criado_por')
            email_prestador = c.get('prestador')
            
            c['nome_criador'] = mapa_nomes.get(email_criador, "Usuário Externo")
            c['nome_prestador'] = mapa_nomes.get(email_prestador, "Ainda não atribuído")
            
            if c['status'] in ['Em Análise', 'Em Execução', 'Resolvido', 'Encerrado'] and not email_prestador:
                c['nome_prestador'] = "Prestador Geral"

        return chamados