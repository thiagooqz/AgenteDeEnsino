import time
import json
import os
import google.generativeai as genai

API_KEY = "CHAVE API"

class UserProgress:
    def __init__(self, username):
        self.username = username
        self.progress_file = f"{username}_progress.json"
        self.progress = self.load_progress()

    def load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            "current_level": 1,
            "completed_topics": {},
            "topic_levels": {},
            "total_points": 0,
            "achievements": []
        }

    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f)

    def get_topic_level(self, subject, topic):
        key = f"{subject}_{topic}"
        return self.progress["topic_levels"].get(key, 1)

    def update_topic_progress(self, subject, topic, score):
        key = f"{subject}_{topic}"
        current_level = self.progress["topic_levels"].get(key, 1)
        
        points_earned = score * current_level
        self.progress["total_points"] += points_earned
        
        if score >= 60:
            if current_level < 5:
                self.progress["topic_levels"][key] = current_level + 1
                self.progress["achievements"].append(f"Avançou para o nível {current_level + 1} em {topic}")
        
        self.save_progress()
        return points_earned

def temas_por_disciplina(disciplina):
    temas = {
        "portugues": [
            "Interpretação de texto",
            "Interpretação de texto não verbal",
            "Gêneros textuais",
            "Variação Linguística",
            "Figuras de Linguagem",
            "Intertextualidade",
            "Funções da linguagem",
            "Semântica",
            "Norma culta e coloquial",
            "Morfologia",
            "Sintaxe",
            "Literatura e Movimentos literários",
            "Obras literárias",
            "Poesias Concretas"
        ],
        "English": [
            "Verb Tenses",
            "Modals",
            "Verbal Voices",
            "Conjunctions",
            "Pronouns",
            "Text Interpretation"
        ],
        "español": [
            "Semántica",
            "Interpretación",
            "Función del Texto",
            "Figuras Retóricas",
            "Artes"
        ],
        "historia": [
            "Brasil República",
            "Segundo Reinado",
            "Mundo Contemporâneo",
            "Primeira Guerra Mundial",
            "Brasil Colonial",
            "Mundo medieval",
            "Povos tradicionais brasileiros",
            "Nazismo e fascismo",
            "Antiguidade Clássica: Grécia e Roma",
            "Revolução Industrial",
            "Segunda Guerra Mundial",
            "Idade Média",
            "Ditadura Militar",
            "Patrimônio histórico e cultural"
        ],
        "geografia": [
            "Meio ambiente e sustentabilidade",
            "Agropecuária",
            "Urbanização",
            "Comércio",
            "Globalização",
            "Geografia física",
            "População",
            "Hidrografia",
            "Geopolítica",
            "Imigrações",
            "Climatologia"
        ],
        "sociologia": [
            "Cidadania",
            "Mundo do Trabalho",
            "Movimentos sociais",
            "Correntes teóricas",
            "Diversidade cultural",
            "Desigualdade social"
        ],
        "filosofia": [
            "Filosofia antiga",
            "Filosofia medieval",
            "Teoria do conhecimento",
            "Política moderna",
            "Filosofia contemporânea"
        ],
        "fisica": [
            "Mecânica",
            "Eletricidade e magnetismo",
            "Termodinâmica",
            "Óptica",
            "Ondulatória",
            "Física moderna"
        ],
        "quimica": [
            "Eletroquímica",
            "Matéria e suas Transformações",
            "Soluções",
            "Estequiometria",
            "Reações Orgânicas"
        ],
        "biologia": [
            "Fisiologia humana",
            "Biotecnologia",
            "Biologia celular",
            "Botânica",
            "Ecologia",
            "Seres vivos",
            "Citologia",
            "Genética",
            "Anatomia e Fisiologia"
        ],
        "proporcionalidade": [
            "Razão e Proporção",
            "Grandezas proporcionais",
            "Regra de três simples",
            "Regra de três composta",
            "Porcentagem"
        ],
        "estatistica": [
            "Média aritmética",
            "Moda e Mediana",
            "Gráficos e tabelas",
            "Probabilidade",
            "Análise combinatória"
        ],
        "geometria": [
            "Geometria Plana",
            "Geometria Espacial",
            "Trigonometria",
            "Áreas e Volumes",
            "Perímetros"
        ],
        "algebra": [
            "Funções",
            "Equações e Inequações",
            "Matemática Financeira",
            "Progressões",
            "Matrizes e Determinantes"
        ]
    }
    return temas.get(disciplina, [])

def get_level_content(tema, nivel, lingua="portugues"):
    nivel_content = {
        1: {
            "difficulty": "básico",
            "content_depth": "conceitos fundamentais",
            "exercise_complexity": "baixa",
            "content_focus": "introdução e definições básicas",
            "example_complexity": "simples e diretos"
        },
        2: {
            "difficulty": "intermediário básico",
            "content_depth": "aplicações simples",
            "exercise_complexity": "média-baixa",
            "content_focus": "compreensão e aplicação básica",
            "example_complexity": "contextualizados simples"
        },
        3: {
            "difficulty": "intermediário",
            "content_depth": "aplicações complexas",
            "exercise_complexity": "média",
            "content_focus": "análise e interpretação",
            "example_complexity": "contextualizados complexos"
        },
        4: {
            "difficulty": "intermediário avançado",
            "content_depth": "análise crítica",
            "exercise_complexity": "média-alta",
            "content_focus": "análise crítica e resolução de problemas",
            "example_complexity": "interdisciplinares"
        },
        5: {
            "difficulty": "avançado",
            "content_depth": "domínio completo",
            "exercise_complexity": "alta",
            "content_focus": "síntese e avaliação",
            "example_complexity": "complexos e interdisciplinares"
        }
    }
    return nivel_content[nivel]

def configurar_api():
    genai.configure(api_key=API_KEY)

def mostrar_menu(user_progress):
    print(f"\nBem-vindo ao Assistente ENEM, {user_progress.username}!")
    print(f"Pontuação Total: {user_progress.progress['total_points']}")
    print("\nSelecione uma área de conhecimento para estudar:")
    print("1. Linguagens")
    print("2. Ciências Humanas")
    print("3. Ciências da Natureza")
    print("4. Matemática")
    print("5. Ver Progresso")
    print("6. Cronômetro de Estudos")
    print("7. Sair")

def submenu_linguagens():
    print("\nSelecione a língua que deseja estudar:")
    print("1. Português")
    print("2. Inglês")
    print("3. Espanhol")
    print("4. Voltar")

def submenu_humanas():
    print("\nSelecione a disciplina que deseja estudar:")
    print("1. História")
    print("2. Geografia")
    print("3. Sociologia")
    print("4. Filosofia")
    print("5. Voltar")

def submenu_natureza():
    print("\nSelecione a disciplina que deseja estudar:")
    print("1. Física")
    print("2. Química")
    print("3. Biologia")
    print("4. Voltar")

def submenu_matematica():
    print("\nTópicos de Matemática:")
    print("1. Proporcionalidade")
    print("2. Estatística")
    print("3. Geometria")
    print("4. Álgebra")
    print("5. Voltar")

def mostrar_progresso(user_progress):
    print("\n=== SEU PROGRESSO ===")
    print(f"Pontuação Total: {user_progress.progress['total_points']}")
    print("\nNível por Tópico:")
    for topic_key, level in user_progress.progress["topic_levels"].items():
        subject, topic = topic_key.split("_", 1)
        print(f"{subject} - {topic}: Nível {level}")
    
    print("\nConquistas Recentes:")
    for achievement in user_progress.progress["achievements"][-5:]:
        print(f"- {achievement}")

def consultar_api_gemini(tema, nivel, lingua="portugues"):
    try:
        model = genai.GenerativeModel('gemini-pro')
        nivel_info = get_level_content(tema, nivel)
        
        prompt_conteudo = f"""
        Explique o tema '{tema}' do ENEM {lingua} considerando:
        - Nível de dificuldade: {nivel_info['difficulty']}
        - Profundidade: {nivel_info['content_depth']}
        - Foco do conteúdo: {nivel_info['content_focus']}
        - Complexidade dos exemplos: {nivel_info['example_complexity']}
        
        O conteúdo deve ser progressivo em relação aos níveis anteriores, sem repetir conceitos básicos já abordados.
        Inclua exemplos práticos e aplicações do conteúdo.
        """
        
        response_conteudo = model.generate_content(prompt_conteudo)
        
        prompt_exercicios = f"""
        Gere 10 questões de múltipla escolha sobre {tema} considerando:
        - Nível de dificuldade: {nivel_info['difficulty']}
        - Complexidade: {nivel_info['exercise_complexity']}
        - Foco: {nivel_info['content_focus']}
        
        As questões devem ser progressivamente mais complexas que os níveis anteriores e
        incluir contextualizações relevantes para o ENEM.
        
        Formate cada questão assim:
        QUESTÃO X:
        [enunciado]
        
        A) [alternativa]
        B) [alternativa]
        C) [alternativa]
        D) [alternativa]
        E) [alternativa]
        """
        
        response_exercicios = model.generate_content(prompt_exercicios)
        
        prompt_respostas = f"""
        Para as questões fornecidas, gere respostas detalhadas incluindo:
        - Letra da alternativa correta
        - Explicação completa da resposta
        - Conceitos fundamentais envolvidos
        - Conexões com outros temas e aplicações práticas
        
        {response_exercicios.text}
        
        Formate cada resposta assim:
        QUESTÃO X:
        Resposta: [letra]
        Explicação: [explicação detalhada]
        """
        
        response_respostas = model.generate_content(prompt_respostas)
        
        return (response_conteudo.text, response_exercicios.text, response_respostas.text)
    except Exception as e:
        return f"Erro: {e}", "", ""

def realizar_exercicios(exercicios, respostas):
    questoes = exercicios.split("QUESTÃO")[1:]
    respostas_corretas = []
    respostas_usuario = []
    
    for i, questao in enumerate(questoes[:10], 1):
        print(f"\nQUESTÃO {i}:")
        print(questao.strip())
        
        while True:
            resposta = input("Sua resposta (A-E): ").upper()
            if resposta in ['A', 'B', 'C', 'D', 'E']:
                break
            print("Por favor, digite uma letra válida (A, B, C, D ou E)")
        
        respostas_usuario.append(resposta)
        
        try:
            resposta_correta = respostas.split(f"QUESTÃO {i}:")[1].split("Resposta: ")[1].split("\n")[0].strip()
            respostas_corretas.append(resposta_correta)
            
            print("\nExplicação:")
            explicacao = respostas.split(f"QUESTÃO {i}:")[1].split("Explicação: ")[1].split("QUESTÃO")[0].strip()
            print(explicacao)
            
            if resposta == resposta_correta:
                print("\n✓ Correto!")
            else:
                print(f"\n✗ Incorreto. A resposta correta é {resposta_correta}")
            
            input("\nPressione Enter para continuar...")
            
        except Exception as e:
            print(f"Erro ao processar resposta: {e}")
            continue
    
    acertos = sum(1 for u, c in zip(respostas_usuario, respostas_corretas) if u == c)
    score = (acertos / len(respostas_usuario)) * 100
    
    print(f"\nResultado Final:")
    print(f"Acertos: {acertos}/10")
    print(f"Aproveitamento: {score:.1f}%")
    
    if score >= 60:
        print("Parabéns! Você atingiu a pontuação necessária para avançar!")
    else:
        print("Continue praticando para atingir a pontuação necessária (60%)")
    
    return score

def mostrar_temas_e_consultar(disciplina, temas, user_progress, lingua="portugues"):
    while True:
        print(f"\nTemas em {disciplina}:")
        for i, tema in enumerate(temas, 1):
            nivel_atual = user_progress.get_topic_level(disciplina, tema)
            print(f"{i}. {tema} (Nível atual: {nivel_atual}/5)")
        
        print("\nEscolha um tema (0 para voltar):")
        escolha = input("Digite o número do tema: ")
        
        if escolha == "0":
            break
        
        if escolha.isdigit() and 1 <= int(escolha) <= len(temas):
            tema_selecionado = temas[int(escolha) - 1]
            nivel_atual = user_progress.get_topic_level(disciplina, tema_selecionado)
            
            while True:  
                print(f"\nEstudando {tema_selecionado} - Nível {nivel_atual}/5")
                
                conteudo, exercicios, respostas = consultar_api_gemini(
                    tema_selecionado,
                    nivel_atual,
                    lingua
                )
                
                print("\nConteúdo do nível:", nivel_atual)
                print(conteudo)
                
                print("\nDeseja resolver exercícios sobre este tema? (S/N)")
                if input().lower() == 's':
                    print("\n=== EXERCÍCIOS ===")
                    score = realizar_exercicios(exercicios, respostas)
                    points = user_progress.update_topic_progress(disciplina, tema_selecionado, score)
                    
                    print(f"\nPontos ganhos: {points}")
                    novo_nivel = user_progress.get_topic_level(disciplina, tema_selecionado)
                    
                    if novo_nivel > nivel_atual:
                        print(f"Parabéns! Você avançou para o nível {novo_nivel}!")
                        if novo_nivel == 5:
                            print("Você atingiu o nível máximo neste tema!")
                    elif score >= 60:
                        print("Excelente! Continue praticando para manter seu nível!")
                    else:
                        print("Continue praticando para avançar de nível!")
                
                print("\nDeseja continuar estudando este tema? (S/N)")
                if input().lower() != 's':
                    break
        else:
            print("\nOpção inválida. Tente novamente.")

def estudar_linguagens(user_progress):
    while True:
        submenu_linguagens()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            temas = temas_por_disciplina("portugues")
            mostrar_temas_e_consultar("Português", temas, user_progress, "portugues")
        elif opcao == "2":
            temas = temas_por_disciplina("ingles")
            mostrar_temas_e_consultar("Inglês", temas, user_progress, "ingles")
        elif opcao == "3":
            temas = temas_por_disciplina("espanhol")
            mostrar_temas_e_consultar("Espanhol", temas, user_progress, "espanhol")
        elif opcao == "4":
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def estudar_humanas(user_progress):
    while True:
        submenu_humanas()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            temas = temas_por_disciplina("historia")
            mostrar_temas_e_consultar("História", temas, user_progress)
        elif opcao == "2":
            temas = temas_por_disciplina("geografia")
            mostrar_temas_e_consultar("Geografia", temas, user_progress)
        elif opcao == "3":
            temas = temas_por_disciplina("sociologia")
            mostrar_temas_e_consultar("Sociologia", temas, user_progress)
        elif opcao == "4":
            temas = temas_por_disciplina("filosofia")
            mostrar_temas_e_consultar("Filosofia", temas, user_progress)
        elif opcao == "5":
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def estudar_natureza(user_progress):
    while True:
        submenu_natureza()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            temas = temas_por_disciplina("fisica")
            mostrar_temas_e_consultar("Física", temas, user_progress)
        elif opcao == "2":
            temas = temas_por_disciplina("quimica")
            mostrar_temas_e_consultar("Química", temas, user_progress)
        elif opcao == "3":
            temas = temas_por_disciplina("biologia")
            mostrar_temas_e_consultar("Biologia", temas, user_progress)
        elif opcao == "4":
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def estudar_matematica(user_progress):
    while True:
        submenu_matematica()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            temas = temas_por_disciplina("proporcionalidade")
            mostrar_temas_e_consultar("Proporcionalidade", temas, user_progress)
        elif opcao == "2":
            temas = temas_por_disciplina("estatistica")
            mostrar_temas_e_consultar("Estatística", temas, user_progress)
        elif opcao == "3":
            temas = temas_por_disciplina("geometria")
            mostrar_temas_e_consultar("Geometria", temas, user_progress)
        elif opcao == "4":
            temas = temas_por_disciplina("algebra")
            mostrar_temas_e_consultar("Álgebra", temas, user_progress)
        elif opcao == "5":
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def cronometrar():
    print("\nCronômetro de estudo. Digite o tempo em minutos.")
    minutos = input("Minutos: ")
    if minutos.isdigit():
        segundos = int(minutos) * 60
        print(f"Cronômetro iniciado por {minutos} minutos. Boa sorte!")
        time.sleep(segundos)
        print("\nTempo encerrado! Volte ao estudo.")
    else:
        print("Entrada inválida. Voltando ao menu principal.")

def main():
    configurar_api()
    
    print("Bem-vindo ao Assistente ENEM!")
    username = input("Digite seu nome de usuário: ")
    user_progress = UserProgress(username)
    
    while True:
        mostrar_menu(user_progress)
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            estudar_linguagens(user_progress)
        elif opcao == "2":
            estudar_humanas(user_progress)
        elif opcao == "3":
            estudar_natureza(user_progress)
        elif opcao == "4":
            estudar_matematica(user_progress)
        elif opcao == "5":
            mostrar_progresso(user_progress)
        elif opcao == "6":
            cronometrar()
        elif opcao == "7":
            print("\nObrigado por estudar conosco!")
            break
        else:
            print("\nOpção inválida!")

if __name__ == "__main__":
    main()
