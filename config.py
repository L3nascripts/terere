from typing import Dict

class GerenciadorTemas:
    TEMAS = {
        "light": {
            "bg": "#FFF4F7",        # Fundo: Off-white levemente rosado (pétalas caídas)
            "fg": "#4A3B3C",        # Texto: Marrom escuro acinzentado (tronco do Tajy)
            "input_bg": "#FFFFFF",  # Entradas: Branco puro para manter a legibilidade
            "btn_bg": "#F0D8DE",    # Botões inativos: Rosa suave
            "accent": "#D81B60",    # Destaque: Rosa/Magenta da flor do Tajy
            "err": "#E53935",       # Erro: Vermelho vivo para contrastar
            "btn_fg": "#FFFFFF"     # Texto dos botões de destaque: Branco
        },
        "dark": {
            "bg": "#1A1C23",        # Fundo: Ardósia escuro (Noite nos Andes)
            "fg": "#E8EAEF",        # Texto: Branco gelo
            "input_bg": "#121419",  # Entradas: Fundo super escuro
            "btn_bg": "#2A2E39",    # Botões inativos: Cinza chumbo
            "accent": "#FCE300",    # Destaque: Amarelo ouro (Bandeira da Bolívia)
            "err": "#FF4C4C",       # Erro: Vermelho luminoso
            "btn_fg": "#1A1C23"     # Texto dos botões de destaque: Escuro
        }
    }
    tema_ativo = "light"

    @classmethod
    def alternar(cls) -> None:
        cls.tema_ativo = "dark" if cls.tema_ativo == "light" else "light"

    @classmethod
    def get(cls) -> Dict[str, str]:
        return cls.TEMAS[cls.tema_ativo]


class GerenciadorIdiomas:
    idioma_ativo = "pt"
    
    TEXTOS = {
        "pt": {
            "dev_by": "Desenvolvido por L3nascripts",
            "login_title": "Terere - Estudo de Guarani 🧉",
            "login_sub": "Selecione ou crie um perfil para salvar seu progresso:",
            "login_btn_enter": "Entrar com Perfil",
            "login_or": "--- ou crie um novo ---",
            "login_btn_new": "Criar Novo Perfil",
            "login_btn_guest": "Entrar em Modo Visitante",
            "title_app": "Terere - Estudo de Guarani 🇵🇾 🇧🇴 🧉",
            "tab_profile": "Meu Perfil", "tab_lab": "Laboratório", "tab_dict": "Dicionário", "tab_quiz": "Praticar", "tab_guide": "Guia Prático",
            "lbl_keyboard": "Teclado Rápido:", "btn_theme": "Alternar Tema", "lbl_lang": "Idioma:", "btn_logout": "Trocar de Usuário",
            "prof_title": "Gestão de Perfil e Progresso", "prof_sel_lbl": "Usuário Atual:", 
            "btn_load": "Carregar", "btn_new": "Criar Novo", "btn_del": "Excluir",
            "prof_guest_warn": "(Modo Visitante: O seu progresso atual não será salvo.)",
            "prof_days": "Dias Estudados (Ofensiva): {}", "prof_quiz_stats": "Desempenho no Praticar: {} Acertos | {} Erros ({}%)",
            "lab_title": "Analisador e Construtor de Palavras", "lab_sub": "Digite a palavra (ex: guata, ndoguatái):",
            "lab_paradigma": "Paradigma:", "btn_conjugate": "Analisar",
            "col_pronoun": "Pronome", "col_present": "Presente", "col_past": "Passado", "col_future": "Futuro",
            "title_dict": "Dicionário Guarani-Português", "subtitle_dict": "Buscar (Guarani/Português):",
            "lbl_total_dict": "Verbetes Traduzidos: {} (Espanhol) | {} (Português)",
            "col_gn": "Guarani", "col_es": "Espanhol", "col_pt": "Português", "col_tipo": "Classe",
            "lbl_ex_gn": "Guarani:", "lbl_ex_es": "Português:",
            "ed_save": "Salvar Palavra", "ed_del_word": "Excluir",
            "quiz_title": "Qual é a tradução correta?", "quiz_score": "Acertos: {} | Erros: {}", "btn_next": "Pular",
            "lbl_base_estudo": "Base de Estudo:", "rad_gn_pt": "Guarani ↔ Português", "rad_gn_es": "Guarani ↔ Espanhol",
            "guide_title": "Guia de Pronúncia e Gramática Base",
            "guide_text": """=== PRONÚNCIA BÁSICA ===
1. Vogais Nasais (ã, ẽ, ĩ, õ, ũ, ỹ): O ar sai pelo nariz e pela boca ao mesmo tempo. A nasalidade é fundamental no Guarani.
2. Y (Vogal Gutural): Não tem som de 'i'. Faça um sorriso forçado e tente dizer 'i' empurrando a base da língua para trás.
3. Puso ('): Oclusiva glotal. Uma pausa brusca na garganta, como a pausa in "uh-oh" no inglês.
4. J: Soa como o "dj" em "dia" (em alguns sotaques) ou o "j" no inglês "John".
5. H: Sempre aspirado, como o "h" na palavra inglesa "house" ou o "rr" suave.
6. Ch: Soa como o nosso "ch/x" em "chave".

=== REGRAS GRAMATICAIS ESSENCIAIS ===
1. Harmonia Nasal: Se a raiz da palavra contém ao menos uma letra nasal, os prefixos e sufixos também se tornam nasais.
   - Exemplo: O prefixo "ja" (nós) vira "ña" em palavras nasais (ñamba'apo).

2. Substantivos Triformes (Oscilantes): Palavras com 'T' inicial mudam sua consoante ao indicar posse:
   - T (Absoluto): Tesa (olho)
   - R (Posse 1ª/2ª pessoa): Che resa (meu olho), Nde resa (teu olho)
   - H (Posse 3ª pessoa): Hesa (olho dele/dela)

=== PARADIGMAS VERBAIS ===
1. Paradigma Areal (Verbos de Ação Padrão): Indicam ações diretas. Utilizam os prefixos a-, re-, o-, ja-/ña-, ro-, pe-. 
   - Exemplo: aguata (eu caminho).

2. Paradigma Aireal (Ação com "i"): Semelhante ao Areal, mas exige a vogal "i" no prefixo: ai-, rei-, oi-, jai-/ñai-, roi-, pei-. 
   - Exemplo: aipota (eu quero).

3. Paradigma Chendal (Qualitativos/Estado): Não se usa verbo de ligação ("ser/estar"). O pronome se junta ao estado/adjetivo: che, nde/ne, i/iñ, ñande/ñane, ore, pende/pene. 
   - Exemplo: Che vare'a (Estou com fome); Nde porã (Você é bonito/a)."""
        },
        "es": {
            "dev_by": "Desarrollado por L3nascripts",
            "login_title": "Terere - Estudio de Guaraní 🧉",
            "login_sub": "Seleccione o cree un perfil para guardar su progreso:",
            "login_btn_enter": "Entrar con Perfil",
            "login_or": "--- o cree uno nuevo ---",
            "login_btn_new": "Crear Nuevo Perfil",
            "login_btn_guest": "Entrar en Modo Invitado",
            "title_app": "Terere - Estudio de Guaraní 🇵🇾 🇧🇴 🧉",
            "tab_profile": "Mi Perfil", "tab_lab": "Laboratorio", "tab_dict": "Diccionario", "tab_quiz": "Practicar", "tab_guide": "Guía Práctica",
            "lbl_keyboard": "Teclado Rápido:", "btn_theme": "Cambiar Tema", "lbl_lang": "Idioma:", "btn_logout": "Cambiar Usuario",
            "prof_title": "Gestión de Perfil y Progreso", "prof_sel_lbl": "Usuario Actual:", 
            "btn_load": "Cargar", "btn_new": "Crear Nuevo", "btn_del": "Eliminar",
            "prof_guest_warn": "(Modo Invitado: Su progreso no se guardará.)",
            "prof_days": "Días Estudiados (Racha): {}", "prof_quiz_stats": "Desempeño en Práctica: {} Aciertos | {} Errores ({}%)",
            "lab_title": "Analizador y Constructor de Palabras", "lab_sub": "Escriba la palabra (ej: guata, ndoguatái):",
            "lab_paradigma": "Paradigma:", "btn_conjugate": "Analizar",
            "col_pronoun": "Pronombre", "col_present": "Presente", "col_past": "Pasado", "col_future": "Futuro",
            "title_dict": "Diccionario Guaraní-Español", "subtitle_dict": "Buscar (Guaraní/Español):",
            "lbl_total_dict": "Palabras Traducidas: {} (Español) | {} (Portugués)",
            "col_gn": "Guaraní", "col_es": "Español", "col_pt": "Portugués", "col_tipo": "Clase",
            "lbl_ex_gn": "Guaraní:", "lbl_ex_es": "Español:",
            "ed_save": "Guardar Palabra", "ed_del_word": "Eliminar",
            "quiz_title": "¿Cuál es la traducción correcta?", "quiz_score": "Aciertos: {} | Errores: {}", "btn_next": "Saltar",
            "lbl_base_estudo": "Base de Estudio:", "rad_gn_pt": "Guaraní ↔ Portugués", "rad_gn_es": "Guaraní ↔ Español",
            "guide_title": "Guía de Pronunciación y Gramática",
            "guide_text": """=== PRONUNCIACIÓN BÁSICA ===
1. Vocales Nasales (ã, ẽ, ĩ, õ, ũ, ỹ): El aire sale por la nariz y por la boca al mismo tiempo. La nasalidad es fundamental en el Guaraní.
2. Y (Gutural): No tiene sonido de 'i'. Haga una sonrisa forzada e intente decir 'i' empujando la base de la lengua hacia atrás.
3. Puso ('): Oclusiva glotal. Una pausa brusca en la garganta, como la pausa en "uh-oh" en inglés.
4. J: Suena como la 'y' en Argentina o la 'j' en el inglés "John".
5. H: Siempre aspirada, como la "h" en la palabra inglesa "house" o una "j" suave.
6. Ch: Suena como la "ch" estándar en español.

=== REGLAS GRAMATICALES ESENCIALES ===
1. Armonía Nasal: Si la raíz de la palabra contiene al menos una letra nasal, los prefijos y sufijos también se vuelven nasales.
   - Ejemplo: El prefijo "ja" (nosotros) se convierte en "ña" en palabras nasales (ñamba'apo).

2. Sustantivos Triformes (Oscilantes): Palabras con 'T' inicial cambian su consonante al indicar posesión:
   - T (Absoluto): Tesa (ojo)
   - R (Posesión 1ª/2ª persona): Che resa (mi ojo), Nde resa (tu ojo)
   - H (Posesión 3ª persona): Hesa (ojo de él/ella)

=== PARADIGMAS VERBALES ===
1. Paradigma Areal (Verbos de Acción Estándar): Indican acciones directas. Utilizan los prefijos a-, re-, o-, ja-/ña-, ro-, pe-. 
   - Ejemplo: aguata (yo camino).

2. Paradigma Aireal (Acción con "i"): Similar al Areal, pero exige la vocal "i" en el prefijo: ai-, rei-, oi-, jai-/ñai-, roi-, pei-. 
   - Ejemplo: aipota (yo quiero).

3. Paradigma Chendal (Cualitativos/Estado): No se usa verbo de enlace ("ser/estar"). El pronombre se une al estado/adjetivo: che, nde/ne, i/iñ, ñande/ñane, ore, pende/pene. 
   - Ejemplo: Che vare'a (Estoy con hambre); Nde porã (Eres lindo/a)."""
        },
        "gn": {
            "dev_by": "Ojapóva L3nascripts",
            "login_title": "Terere - Ñe'ẽkuaaty Rembipuru 🧉",
            "login_sub": "Eiporavo térã eikytĩ peteĩ ava ñongatu haguã:",
            "login_btn_enter": "Eike Ava Ndive",
            "login_or": "--- térã eikytĩ pyahu ---",
            "login_btn_new": "Eikytĩ Ava Pyahu",
            "login_btn_guest": "Eike Mbohupa Rekópe",
            "title_app": "Terere - Ñe'ẽkuaaty Rembipuru 🇵🇾 🇧🇴 🧉",
            "tab_profile": "Che Tembiasa", "tab_lab": "Ñe'ẽ Kuaaty", "tab_dict": "Ñe'ẽndy", "tab_quiz": "Ñembosarái", "tab_guide": "Marandu",
            "lbl_keyboard": "Jekutyha:", "btn_theme": "Sa'y", "lbl_lang": "Ñe'ẽ:", "btn_logout": "Ava Moambue",
            "prof_title": "Che Rembiapo Ykaha", "prof_sel_lbl": "Ava:", 
            "btn_load": "Eike", "btn_new": "Pyahu", "btn_del": "Mbogue",
            "prof_guest_warn": "(Mbohupa rekópe: Tembiasa ndojeñongatúi.)",
            "prof_days": "Ára Ñemoarandu: {}", "prof_quiz_stats": "Ñembosarái rehegua: {} Oĩ | {} Jejavy ({}%)",
            "lab_title": "Ñe'ẽ Apoha ha Kuaaty", "lab_sub": "Ehai ñe'ẽ (techapyrã: guata, ndoguatái):",
            "lab_paradigma": "Ñe'ẽysaja:", "btn_conjugate": "Moñe'ẽ",
            "col_pronoun": "Terarangue", "col_present": "Ára Agãgua", "col_past": "Ára Mboyvegua", "col_future": "Ára Upeigua",
            "title_dict": "Ñe'ẽndy Avañe'ẽ-Karaiñe'ẽ", "subtitle_dict": "Eheka:",
            "lbl_total_dict": "Ñe'ẽnguéra Oñembohasáva: {} (Karaiñe'ẽ) | {} (Poytugañe'ẽ)",
            "col_gn": "Avañe'ẽ", "col_es": "Karaiñe'ẽ", "col_pt": "Poytugañe'ẽ", "col_tipo": "Ñe'ẽte",
            "lbl_ex_gn": "Avañe'ẽ:", "lbl_ex_es": "Karaiñe'ẽ/Poytugañe'ẽ:",
            "ed_save": "Ñongatu", "ed_del_word": "Mbogue",
            "quiz_title": "Mba'éichapa karaiñe'ẽme?", "quiz_score": "Oĩ porãva: {} | Jejavy: {}", "btn_next": "Ohasáva",
            "lbl_base_estudo": "Ñe'ẽryru:", "rad_gn_pt": "Avañe'ẽ ↔ Poytugañe'ẽ", "rad_gn_es": "Avañe'ẽ ↔ Karaiñe'ẽ",
            "guide_title": "Ñe'ẽpu ha Ñe'ẽtekuaa Kuaaha",
            "guide_text": """=== ÑE'ẼPU ===
1. Pu'ae Tĩgua (ã, ẽ, ĩ, õ, ũ, ỹ): Oñemoñe'ẽ osẽvo yvytu tĩ ha juru rupi. Tekotevẽte avañe'ẽme.
2. Y: Ndoikói 'i'icha. Eñemopukavy ha eha'ã ere 'i' emyatatĩvo ne kũ rapo ahy'o gotyo.
3. Puso ('): Ojoko ñe'ẽ mbeguemi ahy'ópe, "uh-oh" ingyaterrañe'ẽme guáicha.
4. J: Oñemoñe'ẽ 'dj'icha térã "j" ingyaterrañe'ẽme "John" guáicha.
5. H: Ahy'o ryapúpe, "h" ingyaterrañe'ẽme "house" guáicha.
6. Ch: Oñemoñe'ẽ "ch" karaiñe'ẽme guáicha.

=== ÑE'ẼTEKUAA ===
1. Tĩgua ha Jurugua: Ñe'ẽrapo tĩgua omoambue ñe'ẽpehẽngue ijereregua tĩguápe avei.
   - Techapyrã: Ñe'ẽpehẽngue "ja" oiko chugui "ña" ñe'ẽ tĩguápe (ñamba'apo).

2. Tero Mbohapy Ysajáva (Triforme): Tero oñepyrũva "T"-pe omoambue ipu ohechauka vove mba'e jára:
   - T (Ijeheguíva): Tesa (tesa)
   - R (Che/Nde mba'e): Che resa (che resa), Nde resa (nde resa)
   - H (I/Imba'e): Hesa (hesa)

=== ÑE'ẼTE YSAJA (PARADIGMAS) ===
1. Ysaja Areal (Tembiapo): Ohechauka tembiapo tee. Oipuru ñe'ẽpehẽngue a-, re-, o-, ja-/ña-, ro-, pe-. 
   - Techapyrã: aguata.

2. Ysaja Aireal (Tembiapo "i" ndive): Ysaja Areal joguaha, hakatu ojerure pu'ae "i" ñe'ẽpehẽnguépe: ai-, rei-, oi-, jai-, ñai-, roi-, pei-. 
   - Techapyrã: aipota.

3. Ysaja Chendal (Teroja Ñe'ẽtéva): Ndoipurúi ñe'ẽte mojoajuha ("ser/estar" karaiñe'ẽme). Terarangue oñembojoaju terojare: che, nde/ne, i/iñ, ñande/ñane, ore, pende/pene. 
   - Techapyrã: Che vare'a; Nde porã."""
        }
    }
