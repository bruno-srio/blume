# -*- coding: utf-8 -*-
"""Constrói o relatório do projeto Blume (parte 1: pré-textuais ao capítulo 6)."""
import os
from docx.shared import Pt
from docx_kit import Report

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(ROOT, "figures")
OUT = os.path.join(ROOT, "Blume_Relatorio_Projeto_Final.docx")

r = Report()


# ============================================================ CAPA
def capa():
    r.p()
    p = r.p("[NOME DA INSTITUIÇÃO]", align="center", size=13, bold=True)
    p.paragraph_format.space_after = Pt(2)
    p = r.p("[FACULDADE / DEPARTAMENTO]", align="center", size=11.5)
    p.paragraph_format.space_after = Pt(2)
    p = r.p("[CURSO — Licenciatura em Engenharia Informática]", align="center", size=11.5)
    p.paragraph_format.space_after = Pt(0)

    for _ in range(3):
        r.p()

    p = r.p("Blume", align="center", size=34, bold=True)
    p.paragraph_format.space_after = Pt(4)
    p = r.p("Conceção e Implementação de uma Plataforma\nMulti-inquilino de Gestão para Agências",
            align="center", size=15)
    p.paragraph_format.space_after = Pt(6)
    p = r.p("Relatório de Projeto Final de Licenciatura", align="center", size=11.5, italic=True)
    p.paragraph_format.space_after = Pt(0)

    for _ in range(4):
        r.p()

    p = r.p("Autor", align="center", size=10.5, italic=True)
    p.paragraph_format.space_after = Pt(1)
    p = r.p("Bruno Ribeiro", align="center", size=13, bold=True)
    p.paragraph_format.space_after = Pt(1)
    p = r.p("Número de estudante: [NÚMERO]", align="center", size=10.5)
    p.paragraph_format.space_after = Pt(14)

    p = r.p("Orientador", align="center", size=10.5, italic=True)
    p.paragraph_format.space_after = Pt(1)
    p = r.p("[NOME DO ORIENTADOR]", align="center", size=12)
    p.paragraph_format.space_after = Pt(0)

    for _ in range(3):
        r.p()

    p = r.p("Ano letivo [ANO LETIVO]", align="center", size=10.5)
    p.paragraph_format.space_after = Pt(1)
    p = r.p("Agosto de 2026", align="center", size=10.5)
    p.paragraph_format.space_after = Pt(0)
    r.page_break()


# ============================================================ RESUMO
def resumo():
    r.h(1, "Resumo")
    r.p(
        "O Blume é uma aplicação web que dá a uma agência digital um único espaço de trabalho para "
        "gerir a sua própria organização e as contas dos clientes que serve. O projeto foi realizado "
        "como projeto final de licenciatura e teve origem numa experiência anterior: antes de "
        "ingressar no curso, construí o site de um cliente na plataforma Wix enquanto trabalhava como "
        "designer gráfico independente. O controlo reduzido que a plataforma oferecia sobre o site "
        "gerado tornava difícil atuar sobre as recomendações produzidas por ferramentas como o Google "
        "PageSpeed Insights. Daí resultou o interesse em construir um sistema em que as "
        "características técnicas dos sites gerados ficassem sob controlo do programador."
    )
    r.p(
        "O desenvolvimento partiu de um tutorial em vídeo de acesso público, usado como referência "
        "inicial de arquitetura, de modelo de domínio e de sequência de construção. O material "
        "tinha cerca de um ano e várias das bibliotecas envolvidas tinham entretanto lançado versões "
        "maiores com alterações de API, pelo que as instruções originais deixaram de produzir um "
        "sistema funcional. A implementação exigiu reproduzir as falhas, ler a documentação atual de "
        "cada biblioteca, decidir caso a caso entre fixar uma versão antiga e adaptar-se à nova, e "
        "reescrever as partes afetadas. Esse trabalho de diagnóstico, adaptação e decisão é o "
        "desenvolvimento propriamente dito, e está documentado nos capítulos 8 e 9."
    )
    r.p(
        "O sistema é uma aplicação `Next.js 14` escrita em `TypeScript`, que usa o App Router com "
        "React Server Components e Server Actions, `Prisma` sobre `MySQL` para persistência, `Clerk` "
        "para autenticação e `UploadThing` para armazenamento de ficheiros. Estão implementados o "
        "site público de divulgação, a autenticação com proteção ao nível da rota, o controlo de "
        "acessos baseado em papéis, o registo de agências com formulários validados e carregamento de "
        "logótipo, o mecanismo de convites para adesão a uma agência existente, o registo de "
        "atividade e a criação de subcontas."
    )
    r.p(
        "O projeto está em desenvolvimento ativo, e este relatório descreve o estado atual e não um "
        "produto fechado. O esquema de dados declara 23 modelos e descreve o domínio completo, "
        "incluindo CRM, funis, multimédia e faturação; a fundação multi-inquilino está construída e "
        "as áreas funcionais estão a ser desenvolvidas sobre ela. Distingue-se o que já está "
        "implementado, o que está em desenvolvimento, o que está planeado e o que são ideias em "
        "aberto. A validação até agora tem sido manual e estática, apoiada em `TypeScript` e "
        "`ESLint`; testes automatizados estão planeados. São descritos a arquitetura, o modelo de "
        "dados, a implementação, os principais problemas técnicos resolvidos e os fluxos de trabalho "
        "assistidos por IA desenhados para automatizar tarefas recorrentes de desenvolvimento."
    )

    r.h(2, "Palavras-chave", in_toc=False)
    r.p("Desenvolvimento de aplicações web; multi-inquilino; Next.js; Prisma ORM; autenticação e "
        "autorização; projeto final de licenciatura.")
    r.page_break()


# ============================================================ PRÉ-TEXTUAIS
def pre_textuais():
    r.toc()
    r.page_break()
    r.list_of("Lista de Figuras", "Figura")
    r.p()
    r.list_of("Lista de Tabelas", "Tabela")
    r.page_break()


# ============================================================ 1 INTRODUÇÃO
def cap1():
    r.h(1, "1. Introdução")

    r.h(2, "1.1 Contexto")
    r.p(
        "Uma agência digital que constrói e mantém sites para clientes tende a acumular ferramentas "
        "mal articuladas entre si: um sistema para o site do cliente, outro para registar contactos, "
        "um terceiro para guardar material gráfico e uma folha de cálculo para saber quem tem acesso "
        "a quê. Cada cliente precisa do seu próprio espaço isolado, mas a agência precisa de um único "
        "ponto a partir do qual consiga ver e administrar todos eles."
    )
    r.p(
        "O Blume é uma tentativa de construir esse ponto único. É uma aplicação web multi-inquilino "
        "em que a agência é o inquilino de topo, detendo uma equipa de utilizadores e um conjunto de "
        "subcontas. Cada subconta representa um cliente e destina-se a conter os sites, contactos, "
        "funis de venda e ficheiros multimédia desse cliente. O nome é uma escolha de marca inspirada "
        "na empresa fictícia com o mesmo nome da série de jogos *Watch Dogs*; o projeto não tem "
        "qualquer outra ligação a essa obra nem é um projeto relacionado com jogos."
    )

    r.h(2, "1.2 Origem da ideia")
    r.p(
        "O projeto não começou com um enunciado formal de problema. Durante a pesquisa de material "
        "sobre desenvolvimento de software encontrei um tutorial em vídeo extenso sobre uma pilha "
        "tecnológica moderna, parte do qual tratava de um construtor de sites. Essa componente "
        "específica interessou-me por ligação a uma experiência profissional anterior, e o tutorial "
        "passou a servir de ponto de partida — um modelo de domínio e uma pilha já articulados, a "
        "partir dos quais o desenvolvimento próprio se organizou."
    )
    r.p(
        "Antes de estudar Informática trabalhei como designer gráfico independente, e um dos meus "
        "clientes precisava de um site. Nessa altura não sabia programar, pelo que construí o site "
        "com o Wix. A plataforma permitiu produzir um resultado visualmente aceitável sem escrever "
        "código, mas revelou-se frustrante num aspeto concreto: ao tentar melhorar o desempenho "
        "medido do site, não tinha praticamente margem de manobra. O Google PageSpeed Insights "
        "assinalava problemas causados por marcação, scripts e carregamento de recursos que eu não "
        "conseguia ver nem alterar. O que ficou dessa experiência foi a distância entre aquilo que a "
        "ferramenta mandava corrigir e aquilo que a plataforma deixava corrigir."
    )
    r.p(
        "É essa experiência que torna a componente de construção de sites interessante e não apenas "
        "conveniente. Sugeria um projeto em que a plataforma geradora dos sites estivesse ela própria "
        "sob o meu controlo, de modo que as decisões sobre renderização, marcação e entrega de "
        "recursos fossem decisões de desenho e não restrições impostas por um fornecedor."
    )

    r.h(2, "1.3 Problema abordado")
    r.p(
        "O problema de engenharia tratado neste projeto é a construção de uma aplicação "
        "multi-inquilino em que várias organizações, cada uma com vários espaços de trabalho de "
        "cliente e com utilizadores de níveis de acesso distintos, coexistem em segurança dentro de "
        "uma única instalação. O problema tem três partes concretas, todas tratadas neste relatório:"
    )
    r.bullets([
        "**Separação de inquilinos.** Os dados de uma agência não podem tornar-se visíveis a outra, e "
        "os dados de uma subconta não podem tornar-se visíveis a um membro da equipa a quem não "
        "tenha sido concedido acesso.",
        "**Identidade e acesso.** Os utilizadores autenticam-se através de um fornecedor de "
        "identidade externo, mas a autorização depende de papéis próprios da aplicação e de permissões "
        "por subconta que esse fornecedor desconhece.",
        "**Encaminhamento de pedidos.** Uma única aplicação tem de servir um site público de "
        "divulgação, uma área administrativa autenticada e, eventualmente, sites de clientes "
        "publicados em subdomínios próprios.",
    ])

    r.h(2, "1.4 Objetivos")
    r.p("Os objetivos abaixo enquadram a fase atual do desenvolvimento e estão formulados ao nível de "
        "um projeto de licenciatura conduzido por um único autor. Correspondem à fundação sobre a "
        "qual as áreas funcionais da plataforma estão a ser construídas.")
    r.bullets([
        "**O1.** Conceber e implementar um modelo de dados relacional capaz de representar uma "
        "agência, a sua equipa, as suas subcontas de cliente e os recursos que lhes pertencem.",
        "**O2.** Implementar autenticação e proteção ao nível da rota com recurso a um fornecedor de "
        "identidade externo, e acrescentar-lhe autorização baseada em papéis próprios da aplicação.",
        "**O3.** Implementar o percurso de registo através do qual um novo utilizador cria uma "
        "agência, incluindo entrada de dados validada e carregamento de imagem.",
        "**O4.** Implementar um mecanismo de convite através do qual utilizadores adicionais aderem a "
        "uma agência existente com um papel definido.",
        "**O5.** Fornecer a infraestrutura de encaminhamento necessária ao alojamento multi-inquilino "
        "por subdomínio.",
        "**O6.** Construir a estrutura base da aplicação (navegação, troca de conta, janelas modais) "
        "sobre a qual as restantes áreas funcionais possam ser construídas.",
        "**O7.** Adquirir experiência prática com uma pilha tecnológica web atual, incluindo a "
        "adaptação a APIs que mudaram desde a referência inicial, e documentar os problemas "
        "técnicos encontrados e as decisões tomadas para os resolver.",
    ])
    r.p("O capítulo 11 avalia cada um destes objetivos face ao estado atual do sistema.")

    r.h(2, "1.5 Âmbito")
    r.p(
        "O esquema da base de dados descreve o produto completo, enquanto o software construído até "
        "agora cobre a fundação sobre a qual esse produto assenta. Este relatório mantém as duas "
        "coisas distintas. Estão implementados e acessíveis pela interface o site de divulgação, a "
        "autenticação, o registo de agências, a aceitação de convites, as definições da agência "
        "incluindo eliminação, a criação de subcontas, o carregamento de ficheiros e a estrutura base "
        "da aplicação. Estão modelados e planeados o subsistema de CRM, os subsistemas de funis e "
        "multimédia, o subsistema de automações e a faturação. O capítulo 6 e o apêndice A detalham "
        "esta distinção entidade a entidade."
    )
    r.p(
        "A funcionalidade de construção de sites, que motivou originalmente o projeto, está planeada "
        "para uma fase posterior. Ainda não tem editor de páginas, renderizador nem mecanismo de "
        "publicação; duas das suas dependências já estão no lugar: as entidades `Funnel`, "
        "`FunnelPage` e `ClassName` no esquema, e a reescrita de subdomínio na camada de "
        "encaminhamento. A secção 13.5 descreve o que essa fase envolve. Uma direção posterior, "
        "ainda sem desenho nem calendário, é desenvolver componentes próprios para esse editor em "
        "vez de depender apenas de blocos genéricos; a secção 13.6 assinala-a como ideia em aberto."
    )

    r.h(2, "1.6 Utilizadores previstos")
    r.p(
        "O sistema representa dois grupos de utilizadores. Os proprietários e administradores de "
        "agência criam a agência, configuram os seus dados, convidam membros da equipa e criam "
        "subcontas de cliente; é este o grupo servido pela aplicação hoje. Os utilizadores e "
        "convidados de subconta estão representados no modelo de dados e na enumeração `Role`, e o "
        "código de encaminhamento já os encaminha para fora da área da agência; a área de subconta "
        "para onde são dirigidos está planeada e é uma das próximas a construir."
    )

    r.h(2, "1.7 Estrutura do relatório")
    r.p(
        "O capítulo 2 desenvolve o enquadramento e a motivação, incluindo o papel do tutorial que "
        "serviu de ponto de partida. O capítulo 3 enuncia os requisitos e o respetivo estado. O "
        "capítulo 4 descreve as tecnologias usadas e as razões da escolha. O capítulo 5 apresenta a "
        "arquitetura e o capítulo 6 o modelo de dados. O capítulo 7 descreve a implementação "
        "subsistema a subsistema. O capítulo 8 descreve o processo de desenvolvimento, incluindo os "
        "fluxos de trabalho assistidos por IA construídos para o apoiar, e o capítulo 9 analisa os "
        "problemas técnicos mais significativos. O capítulo 10 relata a validação realizada, o "
        "capítulo 11 o estado atual do sistema e o capítulo 12 discute-o. O capítulo 13 descreve o "
        "trabalho em curso, o planeado e as ideias em aberto, e o capítulo 14 conclui."
    )
    r.page_break()


# ============================================================ 2 ENQUADRAMENTO
def cap2():
    r.h(1, "2. Enquadramento e Motivação")

    r.h(2, "2.1 Construtores de sites e o compromisso que impõem")
    r.p(
        "Construtores de sites alojados como o Wix, o Squarespace ou o Webflow resolvem um problema "
        "real: permitem que alguém com competências de design mas sem formação em programação "
        "publique um site funcional e alojado. Fazem-no fornecendo num só produto um editor visual, "
        "uma biblioteca de componentes, alojamento e uma camada de gestão de conteúdos."
    )
    r.p(
        "O compromisso é o controlo. A plataforma é dona do resultado. O utilizador compõe uma página "
        "a partir de blocos fornecidos, e é a plataforma que decide em que HTML, CSS e JavaScript essa "
        "composição se traduz, como os recursos são servidos e o que é executado no carregamento da "
        "página. Para o resultado visual, isto é normalmente aceitável. Para as características "
        "técnicas que dependem do código gerado e não do design, não é."
    )

    r.h(2, "2.2 A experiência que motivou o projeto")
    r.p(
        "Este compromisso não é para mim uma observação abstrata. O site de cliente que construí no "
        "Wix antes de iniciar o curso obteve maus resultados quando medido com o Google PageSpeed "
        "Insights, e as recomendações produzidas pela ferramenta estavam quase todas fora do meu "
        "alcance. Podia alterar imagens e texto; não podia alterar a forma como os scripts eram "
        "agrupados, o que era carregado antes da primeira renderização, ou como a página era montada. "
        "Na altura não tinha vocabulário para descrever porquê, nem conhecimento suficiente para "
        "avaliar se o problema era da plataforma ou da minha utilização dela."
    )
    r.p(
        "Parte do valor deste projeto, do ponto de vista pessoal, é ter passado a dispor desse "
        "vocabulário. Compreender renderização no servidor, hidratação, composição de pacotes e "
        "otimização de imagens torna claro tanto o motivo por que um construtor alojado se comporta "
        "como se comporta, como o esforço de engenharia que seria necessário para fazer melhor."
    )
    r.p(
        "Convém ser preciso quanto ao estatuto desta motivação. O que o Blume persegue é o controlo "
        "sobre o código dos sites gerados; que esse controlo se traduza em melhor desempenho medido "
        "é uma hipótese a testar quando a geração de sites estiver implementada. A secção 13.5 "
        "descreve a avaliação que essa fase permitirá fazer."
    )

    r.h(2, "2.3 De construtor de sites a plataforma para agências")
    r.p(
        "O âmbito do projeto deslocou-se cedo, e essa deslocação está visível no modelo de dados. O "
        "tutorial que serviu de ponto de partida está construído em torno de uma plataforma para "
        "agências e não de um construtor de sites para particulares: a entidade de topo é uma "
        "agência, os sites são modelados como funis pertencentes a uma subconta de cliente, e a "
        "funcionalidade envolvente é CRM e gestão de equipa. A construção de sites é uma "
        "funcionalidade de um produto maior e não o produto em si."
    )
    r.p(
        "Adotar essa estrutura foi uma decisão deliberada. Oferecia um problema de engenharia mais "
        "rico e mais realista do que um editor de sites para um só utilizador: multi-inquilino, "
        "controlo de acessos por papéis, fluxos de convite e encaminhamento por subdomínio são "
        "preocupações que um editor isolado não levantaria. A contrapartida é de sequência: a "
        "construção de sites depende da plataforma que a há de alojar, pelo que fica naturalmente "
        "posicionada depois da fundação multi-inquilino. É essa fundação que está construída, e é "
        "para essa funcionalidade que o plano de desenvolvimento aponta."
    )

    r.h(2, "2.4 O tutorial como ponto de partida")
    r.p(
        "O ponto de partida do projeto foi um tutorial em vídeo extenso publicado no canal de YouTube "
        "WebProdigies, que constrói uma plataforma para agências chamada Plura com `Next.js`, "
        "`Prisma`, `Clerk` e `Stripe`. Usá-lo como referência inicial foi uma decisão de método: "
        "fornecia um modelo de domínio coerente e uma seleção de tecnologias já articuladas entre si, "
        "o que permitiu começar a construir em vez de gastar as primeiras semanas apenas a convergir "
        "para uma arquitetura."
    )
    r.p("Da referência inicial vieram:")
    r.bullets([
        "o conceito global do produto e a decomposição em agência e subconta;",
        "o esquema `Prisma` inicial, avaliado e adotado no primeiro commit;",
        "a seleção de tecnologias;",
        "a estrutura geral dos grupos de rotas e a forma do módulo de consultas no servidor;",
        "a linguagem visual da página de divulgação e da estrutura base da aplicação.",
    ])
    r.p(
        "A referência, contudo, não descrevia o estado atual das bibliotecas. O material tinha cerca "
        "de um ano quando o projeto começou e, nesse intervalo, o `Next.js` lançou uma versão maior, "
        "o `React` lançou uma versão maior, o `Clerk` substituiu a API do seu middleware, o "
        "`UploadThing` alterou a API dos seus auxiliares de cliente e o `Prisma` mudou o local onde "
        "recomenda gerar o cliente. Seguir as instruções tal como estavam produzia, na melhor das "
        "hipóteses, código que não compilava e, na pior, comportamentos incorretos sem mensagem de "
        "erro — como o ciclo de redireções da secção 9.2 ou o formulário que falhava silenciosamente "
        "da secção 9.7."
    )
    r.p(
        "O desenvolvimento consistiu em reproduzir e isolar cada falha, ler a documentação atual de "
        "cada biblioteca, decidir caso a caso entre fixar uma versão antiga e adaptar-se à nova, e "
        "reescrever as partes afetadas a partir das APIs em vigor. Em várias situações a solução "
        "original deixou de ser aplicável e foi substituída por uma implementação própria — a "
        "configuração de matchers do middleware, o caminho de import do cliente `Prisma`, a fixação "
        "coordenada de versões e o tratamento de imagens carregadas são exemplos analisados no "
        "capítulo 9."
    )
    r.p(
        "A relação com a fonte foi mudando à medida que o projeto avançava. No início forneceu a "
        "ordem de construção e o esqueleto da pilha. À medida que as APIs divergiam, passou a ser "
        "sobretudo uma descrição de intenção, cuja tradução para as bibliotecas atuais era o "
        "trabalho. Na fase mais recente deixou de ser a fonte da sequência: as funcionalidades "
        "seguintes — barra lateral, seletor de conta, correções de layout, higiene de commits — "
        "foram desenvolvidas a partir do estado do próprio repositório. O capítulo 8 descreve esta "
        "progressão e a Tabela 6 regista, ponto a ponto, onde a implementação atual difere da "
        "referência e porquê."
    )

    r.h(2, "2.5 Posicionamento do projeto")
    r.p(
        "O Blume é um projeto de engenharia: a conceção, adaptação, integração, depuração e avaliação "
        "de uma aplicação web multi-inquilino não trivial, construída sobre uma pilha tecnológica "
        "atual. É esse o critério com que o restante relatório deve ser lido."
    )
    r.page_break()


# ============================================================ 3 REQUISITOS
def cap3():
    r.h(1, "3. Objetivos e Requisitos")
    r.p(
        "Os requisitos abaixo foram reconstruídos a partir do sistema implementado, do esquema da "
        "base de dados e do plano de desenvolvimento. Como o projeto está em desenvolvimento ativo, "
        "cada requisito tem um estado determinado por inspeção do repositório, segundo quatro "
        "categorias que este relatório usa de forma consistente do princípio ao fim."
    )
    r.bullets([
        "**Implementado.** Acessível pela interface, suportado por código no servidor e persistido na "
        "base de dados.",
        "**Em desenvolvimento.** O mecanismo do lado do servidor está construído e a funcionar; falta "
        "a camada que o expõe ao utilizador. É onde o trabalho decorre atualmente.",
        "**Planeado.** Faz parte do plano de desenvolvimento e está representado no modelo de dados "
        "ou na configuração, aguardando implementação.",
        "**Ideia em aberto.** Direção considerada para fases posteriores, ainda sem desenho nem "
        "calendário definidos.",
    ])
    r.p(
        "A fronteira entre as duas primeiras categorias e as duas últimas corresponde, na prática, à "
        "fronteira entre a fundação da plataforma e as suas áreas funcionais. A fundação — modelo "
        "multi-inquilino, identidade, autorização, encaminhamento e registo — está construída; as "
        "áreas funcionais estão a ser construídas por cima dela."
    )

    r.h(2, "3.1 Requisitos funcionais")
    r.table(
        ["ID", "Requisito", "Estado", "Evidência"],
        [
            ["RF1", "Um visitante consegue ver uma página pública de divulgação com o produto e os planos.",
             ("Implementado", True), "`src/app/site/page.tsx`; `pricingCards` em `src/lib/constants.ts`"],
            ["RF2", "Um visitante consegue criar conta e iniciar sessão.",
             ("Implementado", True), "`<SignUp/>` e `<SignIn/>` do Clerk em `/agency/sign-up` e `/agency/sign-in`"],
            ["RF3", "Todas as rotas não públicas exigem sessão autenticada.",
             ("Implementado", True), "`auth.protect()` em `src/middleware.ts`"],
            ["RF4", "Um utilizador autenticado sem agência é encaminhado para um formulário e pode criar uma.",
             ("Implementado", True), "`src/app/(main)/agency/page.tsx`; `upsertAgency`"],
            ["RF5", "Os dados da agência são validados antes da submissão.",
             ("Implementado", True), "Esquema `Zod` com `react-hook-form` em `agency-details.tsx`"],
            ["RF6", "O proprietário da agência consegue carregar um logótipo.",
             ("Implementado", True), "Rota `agencyLogo` do UploadThing; componente `FileUpload`"],
            ["RF7", "O proprietário consegue definir uma meta de subcontas.",
             ("Implementado", True), "`NumberInput` do Tremor ligado a `updateAgencyDetails`"],
            ["RF8", "O proprietário consegue eliminar a agência, com confirmação.",
             ("Implementado", True), "`deleteAgency` com verificação de posse; `AlertDialog`"],
            ["RF9", "Um utilizador com convite pendente adere à agência no primeiro início de sessão.",
             ("Implementado", True), "`verifyAndAcceptInvitation` em `src/lib/queries.ts`"],
            ["RF10", "O acesso à área da agência é restringido por papel.",
             ("Implementado", True), "Verificação em `src/app/(main)/agency/[agencyId]/layout.tsx`"],
            ["RF11", "As ações significativas são registadas como notificações de atividade.",
             ("Implementado", True), "`saveActivityLogsNotification` escreve registos `Notification`"],
            ["RF12", "O proprietário consegue criar uma subconta de cliente a partir da interface.",
             ("Implementado", True), "`SubAccountDetails` em modal; `upsertSubAccount`"],
            ["RF13", "O utilizador consegue alternar entre a agência e as suas subcontas.",
             ("Em desenvolvimento", True), "O seletor e as ligações existem; faltam as rotas `/subaccount`"],
            ["RF14", "A barra lateral expõe navegação para as áreas funcionais da agência.",
             ("Em desenvolvimento", True), "São criados e carregados 6 registos `AgencySidebarOption`; falta renderizá-los"],
            ["RF15", "As notificações registadas são apresentadas ao utilizador.",
             ("Em desenvolvimento", True), "`getNotifications` já é chamado no layout; falta a interface"],
            ["RF16", "O painel da agência apresenta informação da agência.",
             ("Em desenvolvimento", True), "`[agencyId]/page.tsx` renderiza o identificador; os dados já estão disponíveis"],
            ["RF17", "Os sites publicados são servidos em subdomínio próprio.",
             ("Em desenvolvimento", True), "Reescrita implementada no middleware; páginas `/[domain]` ainda são esboços"],
            ["RF18", "Os utilizadores de subconta têm uma área dedicada.",
             ("Planeado", True), "O destino `/subaccount` está reservado como diretório"],
            ["RF19", "Os clientes são geridos através de pipelines, lanes, tickets e contactos.",
             ("Planeado", True), "Modelos no esquema, com as colunas de ordenação que o Kanban exige"],
            ["RF20", "Os sites são compostos e publicados através de um editor de páginas.",
             ("Planeado", True), "Modelos `Funnel`, `FunnelPage` e `ClassName` já modelados"],
            ["RF21", "Uma biblioteca de multimédia guarda recursos por subconta.",
             ("Planeado", True), "Modelo `Media` e rota `media` do UploadThing já declarada"],
            ["RF22", "As automações são despoletadas por eventos como a submissão de formulários.",
             ("Planeado", True), "Modelos `Trigger`, `Automation`, `AutomationInstance` e `Action`"],
            ["RF23", "As agências são faturadas através de planos de subscrição.",
             ("Planeado", True), "Modelos `Subscription` e `AddOns` e variáveis de ambiente; SDK por integrar"],
        ],
        "Requisitos funcionais e o respetivo estado no repositório atual.",
        widths=[1.0, 5.9, 3.2, 5.4], font_size=8.5,
    )
    r.p(
        "Doze dos vinte e três requisitos estão implementados, cinco estão em desenvolvimento e seis "
        "estão planeados. O grupo em desenvolvimento tem um padrão consistente: em todos os casos o "
        "mecanismo do lado do servidor está construído e a trabalhar, e o que está a ser construído "
        "agora é a camada de interface que o expõe. É essa a frente de trabalho atual."
    )

    r.h(2, "3.2 Requisitos não funcionais")
    r.table(
        ["ID", "Requisito", "Como é assegurado", "Avaliação"],
        [
            ["RNF1", "Segurança de tipos na fronteira cliente/servidor",
             "`TypeScript` em modo estrito; o `Prisma` gera os tipos dos modelos, consumidos "
             "diretamente por formulários e server actions",
             ("Cumprido", True)],
            ["RNF2", "Isolamento de dados entre inquilinos",
             "Todas as leituras são delimitadas pela agência do utilizador autenticado; o acesso por "
             "subconta é regido por registos `Permissions`",
             ("Parcialmente cumprido", True)],
            ["RNF3", "Validação de entrada",
             "Esquemas `Zod` validam os formulários de agência e de subconta antes da submissão",
             ("Cumprido nos formulários existentes", True)],
            ["RNF4", "Manutenibilidade",
             "Organização de diretórios por funcionalidade, um único módulo de server actions, "
             "Conventional Commits, comentários explicativos no código não óbvio",
             ("Parcialmente cumprido", True)],
            ["RNF5", "Usabilidade e adaptação ao ecrã",
             "Pontos de rutura do `Tailwind`; barra fixa em ambiente de secretária e painel deslizante "
             "em dispositivos móveis; temas claro e escuro",
             ("Cumprido nos ecrãs existentes", True)],
            ["RNF6", "Segurança de credenciais e sessões",
             "Gestão de sessão delegada no `Clerk`; segredos em variáveis de ambiente, excluídos do "
             "controlo de versões",
             ("Parcialmente cumprido", True)],
            ["RNF7", "Desempenho das páginas entregues",
             "Componentes de servidor por omissão; `next/image` com padrões remotos configurados; "
             "nenhuma medição realizada",
             ("Não avaliado", True)],
            ["RNF8", "Escalabilidade",
             "Camada aplicacional sem estado; cliente `Prisma` em cache em `globalThis` em "
             "desenvolvimento",
             ("Não avaliado", True)],
            ["RNF9", "Fiabilidade através de testes automatizados",
             "Ainda não está instalada uma framework de testes",
             ("Planeado", True)],
        ],
        "Requisitos não funcionais e o estado atual de cada um.",
        widths=[1.4, 4.2, 7.2, 3.0], font_size=8.5,
    )
    r.p(
        "Duas avaliações merecem nota. O RNF2 está parcialmente cumprido porque, embora todas as "
        "consultas do código estejam corretamente delimitadas pelo inquilino, a verificação de papel "
        "que protege a área da agência lê os metadados da sessão `Clerk` e não a base de dados, e as "
        "rotas do `UploadThing` autenticam quem chama sem associar o carregamento a um inquilino. "
        "Ambos os pontos estão identificados e agendados para correção (secções 12.3 e 13.3). O RNF6 "
        "está parcialmente cumprido porque o tratamento de segredos está estruturalmente correto — o "
        "ficheiro `.env` está excluído do Git — mas os segredos permanecem em texto simples na cópia "
        "de trabalho."
    )

    r.h(2, "3.3 Fronteiras do âmbito")
    r.p(
        "O plano de desenvolvimento é maior do que o que cabe no calendário de um projeto de "
        "licenciatura, pelo que o relatório distingue o que está adiado dentro do plano do que está "
        "fora dele."
    )
    r.p("Planeado para fases posteriores, com o suporte de dados já no lugar:")
    r.bullets([
        "o editor visual de páginas e a renderização dos sites publicados (RF20);",
        "o envio de correio eletrónico, de que depende a emissão de convites pela interface;",
        "a gestão de subscrições e os planos de faturação (RF23), cujos modelos já estão declarados;",
        "a implantação em produção com integração contínua.",
    ])
    r.p("Fora do âmbito do projeto, e por isso não abordado neste relatório:")
    r.bullets([
        "o processamento efetivo de pagamentos e a partilha de receita da plataforma, que envolvem "
        "requisitos legais e financeiros alheios ao objetivo do trabalho;",
        "internacionalização e auditoria formal de acessibilidade.",
    ])
    r.page_break()


# ============================================================ 4 TECNOLOGIAS
def cap4():
    r.h(1, "4. Tecnologias e Ambiente de Desenvolvimento")
    r.p(
        "Este capítulo descreve as tecnologias que determinam a arquitetura. Não enumera "
        "deliberadamente os 64 pacotes do manifesto de dependências; 26 desses são primitivas "
        "individuais do `Radix UI`, arrastadas pela biblioteca de componentes, e não têm significado "
        "arquitetural."
    )

    r.h(2, "4.1 Runtime, framework e linguagem")
    r.p(
        "O `Bun` é usado simultaneamente como runtime de JavaScript e como gestor de pacotes. Foi "
        "adotado porque o tutorial o usava e foi mantido pela instalação de dependências mais rápida, "
        "que é o benefício principal anunciado pelo `Bun`; não foi feita qualquer medição disso no "
        "âmbito do projeto. A escolha teve uma consequência prática: a certa altura foi executado um "
        "comando `npm` por engano, o que produziu um `package-lock.json` ao lado do `bun.lock` "
        "existente. Dois ficheiros de bloqueio a descrever o mesmo grafo de dependências constituem "
        "um risco real, e o ficheiro do `npm` foi removido num commit dedicado."
    )
    r.p(
        "O `Next.js 14.2.24` com App Router fornece encaminhamento, renderização e a fronteira "
        "servidor/cliente. Três das suas funcionalidades determinam a forma da aplicação. Os React "
        "Server Components permitem que as páginas consultem a base de dados diretamente, sem camada "
        "de API intermédia. As Server Actions permitem que componentes de cliente invoquem funções "
        "do servidor como se fossem locais, com a framework a tratar da serialização. O middleware "
        "corre antes de cada pedido correspondido e é onde a autenticação e o encaminhamento "
        "multi-inquilino estão implementados."
    )
    r.p(
        "A escolha da versão 14 em vez da 15 foi imposta e não preferida, conforme descrito na secção "
        "9.1. O `React 18` decorre dessa decisão. O `TypeScript` é usado em modo estrito em todo o "
        "código, o que aqui importa mais do que o habitual porque os tipos que descrevem as linhas da "
        "base de dados são gerados a partir do esquema e fluem diretamente para as definições de "
        "formulários e para as server actions."
    )

    r.h(2, "4.2 Persistência")
    r.p(
        "O `Prisma 6.9.0` é o ORM e o `MySQL` a base de dados. O `Prisma` foi escolhido pela razão "
        "habitual: o ficheiro de esquema é a fonte única de verdade do modelo de dados e o cliente "
        "gerado dá consultas totalmente tipadas. Tanto `prisma` como `@prisma/client` estão fixados "
        "numa versão exata através do campo `overrides` do `package.json`, acrescentado "
        "deliberadamente depois de a divergência de versões entre os dois pacotes causar falhas de "
        "geração."
    )
    r.p(
        "Duas opções de configuração do esquema têm consequências arquiteturais e são examinadas no "
        "capítulo 6: o cliente é gerado em `src/generated/prisma` e não em `node_modules`, e a "
        "datasource define `relationMode = \"prisma\"`, o que transfere a integridade referencial da "
        "base de dados para o ORM."
    )

    r.h(2, "4.3 Identidade")
    r.p(
        "O `Clerk` fornece autenticação como serviço alojado. Disponibiliza componentes prontos de "
        "início de sessão e de registo, gestão de sessão e um auxiliar de middleware que protege "
        "rotas. É também usado como pequena porção de estado aplicacional: `initUser` escreve o papel "
        "do utilizador em `privateMetadata` do utilizador `Clerk`, e o layout da agência lê-o mais "
        "tarde para decidir se renderiza a página ou um aviso de acesso negado."
    )
    r.p(
        "Delegar a autenticação foi a decisão correta para um projeto desta dimensão — a gestão de "
        "sessões e o armazenamento de credenciais são áreas em que uma implementação de estudante "
        "seria quase de certeza pior do que um serviço especializado — mas foi também a maior fonte "
        "isolada de dificuldade do projeto, porque o tutorial usava uma API de middleware anterior. As "
        "secções 9.2 e 9.3 descrevem o custo disso."
    )

    r.h(2, "4.4 Armazenamento de ficheiros")
    r.p(
        "O `UploadThing v7` trata do carregamento de imagens. O servidor declara um file router com "
        "rotas de carregamento nomeadas e as suas restrições, e o cliente usa componentes tipados, "
        "gerados a partir desse router. São declaradas quatro rotas — `agencyLogo`, `subaccountLogo`, "
        "`avatar` e `media` — cada uma aceitando uma imagem de até 4 MB. As duas primeiras estão em "
        "uso; `avatar` e `media` foram declaradas antecipadamente para as funcionalidades planeadas "
        "de perfil de utilizador e biblioteca de multimédia."
    )

    r.h(2, "4.5 Interface")
    r.p(
        "A interface é construída com `Tailwind CSS` e `shadcn/ui`. O `shadcn/ui` não é uma "
        "biblioteca de componentes convencional: copia o código-fonte dos componentes para dentro do "
        "projeto, pelo que os 46 ficheiros em `src/components/ui` são código do projeto e podem ser "
        "editados. Isto revelou-se útil na prática — um desses componentes, o painel deslizante usado "
        "na barra lateral, foi estendido com uma propriedade `showX` para suportar um esquema visual "
        "que o original não previa."
    )
    r.p(
        "Os formulários usam `react-hook-form` com resolvers `Zod`, o que mantém as regras de "
        "validação declarativas e junto às definições dos campos. O `Tremor` contribui com um único "
        "campo numérico usado na meta da agência. O `sonner` fornece notificações temporárias, o "
        "`next-themes` a alternância entre tema claro e escuro, e o `lucide-react` o conjunto de "
        "ícones usado a par dos 31 componentes SVG próprios do projeto."
    )

    r.h(2, "4.6 Ambiente de desenvolvimento")
    r.p(
        "O desenvolvimento decorreu em Fedora Linux com um servidor `MySQL` instalado localmente. O "
        "MySQL Workbench foi usado para inspeção direta da base de dados e, a pedido do orientador, "
        "para uma tentativa de diagrama obtido por engenharia inversa — tentativa que falhou por "
        "razões explicadas na secção 9.6 e que se revelou um dos episódios mais instrutivos do "
        "projeto. O controlo de versões é feito com `Git` e um repositório remoto privado no GitHub. "
        "A edição passou do Visual Studio Code para o Cursor durante o projeto, o que permitiu "
        "construir os fluxos de trabalho assistidos por IA descritos na secção 8.3."
    )

    r.table(
        ["Tecnologia", "Versão", "Papel no Blume"],
        [
            ["`Bun`", "runtime e gestor de pacotes", "Instalação de dependências e execução de scripts"],
            ["`Next.js`", "14.2.24", "App Router, componentes de servidor, server actions, middleware"],
            ["`React`", "18", "Modelo de componentes"],
            ["`TypeScript`", "5", "Tipagem estática em modo estrito em todo o código"],
            ["`prisma` / `@prisma/client`", "6.9.0 (fixada)", "Definição do esquema, aplicação via `db push`, consultas tipadas"],
            ["`MySQL`", "servidor local", "Armazenamento relacional, 23 tabelas"],
            ["`@clerk/nextjs`", "^6.15.0", "Autenticação, sessão, proteção de rotas, papel em metadados"],
            ["`uploadthing` / `@uploadthing/react`", "^7.6.0 / ^7.3.0", "Carregamento de logótipos de agência e subconta"],
            ["`Tailwind CSS`", "^3.4.1", "Estilos e adaptação ao tamanho do ecrã"],
            ["`shadcn/ui` + `Radix UI`", "26 pacotes Radix", "Primitivas acessíveis copiadas para o projeto"],
            ["`react-hook-form` + `Zod`", "^7.55 / ^3.24", "Estado dos formulários e validação por esquema"],
            ["`@tremor/react`", "^3.18.7", "`NumberInput` usado na meta da agência"],
            ["`sonner`, `next-themes`, `lucide-react`", "atuais", "Notificações, tema e ícones"],
        ],
        "Tecnologias principais, com as versões registadas em `package.json`.",
        widths=[4.6, 3.4, 7.8], font_size=8.5,
    )
    r.page_break()


# ============================================================ 5 ARQUITETURA
def cap5():
    r.h(1, "5. Arquitetura do Sistema")

    r.h(2, "5.1 Forma global")
    r.p(
        "O Blume é uma única aplicação `Next.js`. Não há serviço de backend separado, nem API "
        "gateway, nem message broker. A lógica do servidor vive em componentes de servidor, que "
        "correm quando uma página é renderizada, ou em server actions, que correm quando um "
        "componente de cliente as invoca. São usados três serviços externos: `Clerk` para identidade, "
        "`UploadThing` para armazenamento de ficheiros e uma base de dados `MySQL` acedida através do "
        "`Prisma`."
    )
    r.figure(os.path.join(FIG, "fig1_architecture.png"),
             "Arquitetura de alto nível do Blume. Todos os componentes de servidor apresentados "
             "pertencem à mesma instalação `Next.js`; apenas as caixas sombreadas à direita são "
             "externas.", width_cm=15.5)
    r.p(
        "A propriedade mais determinante deste arranjo é a quase ausência de uma API HTTP. A "
        "aplicação expõe exatamente um route handler, `/api/uploadthing`, e existe apenas porque o "
        "fornecedor de carregamentos exige um endpoint de callback. Tudo o resto que convencionalmente "
        "seria um endpoint REST é uma server action. As vantagens são não haver código de "
        "serialização de pedido e resposta para escrever, não haver validação duplicada entre cliente "
        "e servidor, e não haver desvio entre um contrato de API e os seus consumidores. Os custos "
        "são a aplicação não poder ser consumida por nada além do seu próprio frontend, e testar a "
        "lógica do servidor exigir invocar as funções diretamente ou conduzir o browser."
    )

    r.h(2, "5.2 Estrutura de rotas")
    r.p(
        "O App Router organiza as rotas por diretório. O Blume usa grupos de rotas — diretórios entre "
        "parênteses que estruturam a árvore sem contribuir com segmentos de caminho — para dar ao "
        "site de divulgação e à área autenticada layouts diferentes. A Tabela 4 lista todas as rotas "
        "existentes, com o seu propósito e estado."
    )
    r.table(
        ["Rota", "Tipo", "Propósito", "Estado"],
        [
            ["`/`", "redireção", "Redirecionada para `/site` pelo middleware", ("Implementado", True)],
            ["`/site`", "componente de servidor", "Página de divulgação: destaque e três planos", ("Implementado", True)],
            ["`/agency/sign-in/[[...sign-in]]`", "componente de servidor", "Montagem catch-all do `<SignIn/>`", ("Implementado", True)],
            ["`/agency/sign-up/[[...sign-up]]`", "componente de servidor", "Montagem catch-all do `<SignUp/>`", ("Implementado", True)],
            ["`/agency`", "componente de servidor", "Aceitação de convite, redireção por papel, formulário de registo", ("Implementado", True)],
            ["`/agency/[agencyId]`", "componente de servidor", "Painel da agência; renderiza o identificador", ("Em desenvolvimento", True)],
            ["`/agency/unauthorized`", "componente de servidor", "Aviso de acesso negado", ("Implementado", True)],
            ["`/[domain]`", "componente de servidor", "Entrada do site do inquilino; devolve um marcador", ("Em desenvolvimento", True)],
            ["`/[domain]/[path]`", "componente de servidor", "Subpágina do inquilino; devolve um marcador", ("Em desenvolvimento", True)],
            ["`/api/uploadthing`", "route handler", "`GET` e `POST` do file router do UploadThing", ("Implementado", True)],
            ["`/subaccount`", "\u2014", "Área dos utilizadores de subconta; diretório reservado", ("Planeado", True)],
        ],
        "Rotas da aplicação. Os segmentos catch-all nas rotas de autenticação são necessários para "
        "que o `Clerk` possa renderizar os seus fluxos de vários passos por baixo do componente "
        "montado.",
        widths=[5.0, 2.8, 4.5, 3.2], font_size=8.5,
    )
    r.p(
        "A última linha tem uma consequência imediata: tanto a página de registo como o seletor de "
        "conta já ligam para rotas `/subaccount`, pelo que um utilizador de subconta que inicie "
        "sessão encontra um erro 404 até essa área ser construída. A área está planeada e a ordem de "
        "trabalho está na secção 13.4."
    )

    r.h(2, "5.3 A cadeia de middleware")
    r.p(
        "O ficheiro `src/middleware.ts` é, relativamente à sua extensão, o mais carregado do projeto, "
        "e foi também o mais difícil de acertar. Corre em todos os pedidos correspondidos pela sua "
        "configuração e desempenha quatro tarefas distintas: normalizar pontos de entrada, manter "
        "utilizadores autenticados longe dos ecrãs de autenticação, impor autenticação nas rotas "
        "privadas e reescrever pedidos de subdomínio para a rota dinâmica do inquilino. A Figura 2 "
        "mostra a ordem por que estas verificações correm."
    )
    r.figure(os.path.join(FIG, "fig2_middleware.png"),
             "Ordem de processamento de um pedido em `src/middleware.ts`.", width_cm=12.4)
    r.p(
        "A ordem é deliberada e determinante. A autenticação é imposta depois das regras de "
        "redireção, para que um utilizador autenticado que peça a página de início de sessão seja "
        "redirecionado em vez de lhe ser pedida nova autenticação, e antes das regras de reescrita, "
        "para que um pedido anónimo a um subdomínio de inquilino nunca chegue à fase de reescrita. "
        "Errar esta ordem foi a causa direta do ciclo de redireções descrito na secção 9.2."
    )
    r.code([
        "const isPublicRoute = createRouteMatcher([",
        "  '/site',",
        "  '/agency/sign-in(.*)',",
        "  '/agency/sign-up(.*)',",
        "  '/api/uploadthing',",
        "]);",
        "",
        "export default clerkMiddleware(async (auth, req) => {",
        "    /* ... regras de redireção omitidas ... */",
        "    if (!isPublicRoute(req)) {",
        "      await auth.protect();",
        "    }",
        "",
        "    const host = req.headers.get('host') || '';",
        "    const customSubdomain = host",
        "      .split(`${process.env.NEXT_PUBLIC_DOMAIN}`)",
        "      .filter(Boolean)[0];",
        "",
        "    if (customSubdomain) {",
        "      return NextResponse.rewrite(",
        "        new URL(`/${customSubdomain}${pathWithSearch}`, req.url));",
        "    }",
        "    /* ... */",
        "});",
    ], caption="Proteção de rotas e reescrita de subdomínio em `src/middleware.ts`. Os sufixos "
               "`(.*)` nos padrões de autenticação são essenciais: sem eles os fluxos de vários "
               "passos do `Clerk` são tratados como rotas privadas e o pedido entra em ciclo.")

    r.h(2, "5.4 Server actions em vez de uma camada de API")
    r.p(
        "Todo o acesso à base de dados está concentrado em `src/lib/queries.ts`, um módulo marcado "
        "com a diretiva `\"use server\"`. Exporta dez funções assíncronas e mantém um auxiliar "
        "privado. A Tabela 5 lista-as com os respetivos chamadores, o que é também um mapa útil de "
        "quanto do sistema está efetivamente ligado."
    )
    r.table(
        ["Server action", "Responsabilidade", "Chamada a partir de"],
        [
            ["`getAuthUserDetails`", "Carregar o utilizador autenticado com agência, subcontas, opções de barra lateral e permissões",
             "página `/agency`, `Sidebar`"],
            ["`saveActivityLogsNotification`", "Criar um registo `Notification` que descreve uma ação",
             "`agency-details`, `subaccount-details`, `verifyAndAcceptInvitation`"],
            ["`createTeamUser`", "Criar um `User` não proprietário para um membro convidado", "`verifyAndAcceptInvitation`"],
            ["`verifyAndAcceptInvitation`", "Aceitar um convite pendente e devolver o identificador da agência",
             "página `/agency`, layout `[agencyId]`"],
            ["`updateAgencyDetails`", "Atualizar campos selecionados de uma agência", "`agency-details` (meta)"],
            ["`deleteAgency`", "Eliminar uma agência depois de verificar a posse", "`agency-details` (zona de perigo)"],
            ["`initUser`", "Fazer upsert do `User` e escrever o papel nos metadados do `Clerk`", "`agency-details`"],
            ["`upsertAgency`", "Criar ou atualizar uma agência e semear seis opções de barra lateral", "`agency-details`"],
            ["`getNotifications`", "Ler as notificações de uma agência, das mais recentes para as mais antigas", "layout `[agencyId]` (resultado não usado)"],
            ["`upsertSubAccount`", "Criar ou atualizar uma subconta, semear permissões e oito opções de barra lateral",
             "`subaccount-details`"],
            ["`getUser` (privada)", "Resolver um utilizador a partir de uma sessão `Clerk` ou de uma subconta", "não é chamada \u2014 código morto"],
        ],
        "A camada de server actions em `src/lib/queries.ts`.",
        widths=[4.6, 7.0, 5.0], font_size=8.5,
    )

    r.h(2, "5.5 Multi-inquilino e encaminhamento por subdomínio")
    r.p(
        "A separação de inquilinos no Blume opera a dois níveis. Logicamente, a `Agency` é a "
        "fronteira do inquilino: cada utilizador pertence exatamente a uma agência e cada subconta "
        "pertence exatamente a uma agência. Dentro de uma agência, as subcontas são um segundo nível "
        "de isolamento regido por registos `Permissions` explícitos, pelo que um membro da equipa vê "
        "apenas os espaços de cliente a que lhe foi concedido acesso."
    )
    r.p(
        "Fisicamente, todos os inquilinos partilham uma base de dados e uma instalação. O isolamento "
        "é assegurado inteiramente em código aplicacional, delimitando cada consulta pelo utilizador "
        "autenticado. Esta é a mais simples das estratégias multi-inquilino habituais e a adequada a "
        "esta escala, mas concentra toda a garantia de isolamento na construção das consultas: uma "
        "única consulta escrita sem a delimitação correta faria vazar dados entre inquilinos, e nada "
        "na base de dados o impediria."
    )
    r.p(
        "O encaminhamento por subdomínio existe para que um site de cliente publicado possa ser "
        "servido no seu próprio endereço. O middleware divide o cabeçalho `Host` pelo domínio base "
        "configurado e, se sobrar um prefixo, reescreve o pedido para `/[domain]`. O mecanismo "
        "funciona de ponta a ponta; as páginas `/[domain]` são ainda marcadores, à espera do "
        "renderizador de sites. Foram identificados dois passos para completar esta camada: validar "
        "o prefixo extraído contra a coluna `Funnel.subDomainName`, em vez de o derivar apenas de "
        "uma divisão de texto, e devolver uma resposta apropriada para subdomínios desconhecidos."
    )

    r.h(2, "5.6 Implantação")
    r.p(
        "A aplicação corre atualmente apenas em ambiente de desenvolvimento, contra um servidor "
        "`MySQL` local. A implantação está planeada para uma fase posterior e o repositório ainda não "
        "contém configuração de alojamento, definição de contentor ou fluxo de integração contínua."
    )
    r.p(
        "Preparar a implantação depende de dois pré-requisitos já identificados. O primeiro é fazer "
        "passar o build de produção, que falha na fase de análise estática pelas razões dadas na "
        "secção 10.2. O segundo é adotar um histórico de migrações: sem ele, o esquema teria de ser "
        "empurrado para a base de dados de produção em vez de migrado, o que não é aceitável fora de "
        "desenvolvimento. Ambos estão no trabalho de curto prazo da secção 13.3, e a arquitetura de "
        "implantação será desenhada depois de resolvidos."
    )
    r.page_break()


# ============================================================ 6 MODELO DE DADOS
def cap6():
    r.h(1, "6. Modelo de Dados")
    r.p(
        "O esquema em `prisma/schema.prisma` declara 23 modelos e 6 enumerações em 438 linhas. Foi "
        "adotado do tutorial no primeiro commit, depois de avaliado como um modelo coerente para o "
        "domínio pretendido, e serve desde então de mapa do produto a construir. Modelar o domínio "
        "completo à partida foi uma decisão deliberada: dá ao desenvolvimento incremental um destino "
        "estável e evita reestruturações de esquema a cada área funcional nova. A consequência é que "
        "o esquema descreve mais do que a aplicação implementa hoje, pelo que este capítulo separa a "
        "parte já exercitada por código da parte que aguarda implementação."
    )

    r.h(2, "6.1 A cadeia de propriedade")
    r.p(
        "O núcleo do modelo é uma cadeia de propriedade: uma `Agency` detém `User` e `SubAccount`, e "
        "uma `SubAccount` detém os recursos operacionais de um cliente. A Figura 3 mostra as seis "
        "entidades que o código atual efetivamente lê ou escreve."
    )
    r.figure(os.path.join(FIG, "fig4_er_core.png"),
             "Diagrama entidade-relação do núcleo implementado. As listas de atributos estão "
             "abreviadas; as setas apontam da entidade dependente para a entidade referenciada.",
             width_cm=15.5)
    r.p(
        "A `Agency` guarda os dados de contacto e morada da agência, o seu logótipo, um indicador "
        "`whiteLabel` e uma meta para o número de subcontas. A `SubAccount` repete a maior parte "
        "desses campos, duplicação herdada do esquema do tutorial; as duas entidades poderiam "
        "razoavelmente partilhar um tipo comum de organização, mas mantêm-se separadas por "
        "participarem em relações diferentes."
    )
    r.p(
        "O indicador `whiteLabel` é uma pequena porção de lógica de produto codificada no modelo de "
        "dados. Quando está ativo, o logótipo da própria agência é mostrado em todas as interfaces de "
        "subconta; quando não está, cada subconta mostra o seu. A barra lateral implementa esta "
        "regra, e é um dos poucos sítios em que um campo do esquema comanda comportamento visível."
    )

    r.h(2, "6.2 Identidade, papéis e permissões")
    r.p(
        "Os registos `User` espelham as contas `Clerk` em vez de as substituírem. Palavras-passe e "
        "sessões nunca chegam a esta base de dados; a tabela `User` guarda a visão que a aplicação "
        "tem de uma pessoa: o endereço de correio eletrónico, que é único e funciona como chave "
        "natural de ligação entre o `Clerk` e a base de dados, o nome e o avatar, o papel e a agência "
        "a que pertence."
    )
    r.p("A autorização é expressa por dois mecanismos com granularidade diferente:")
    r.bullets([
        "**Papel.** Uma enumeração com quatro valores — `AGENCY_OWNER`, `AGENCY_ADMIN`, "
        "`SUBACCOUNT_USER` e `SUBACCOUNT_GUEST` — guardada no registo `User` e duplicada nos "
        "metadados do `Clerk`. Determina em que área da aplicação o utilizador pode entrar.",
        "**Permissões.** Uma tabela de junção entre o endereço de correio de um utilizador e uma "
        "subconta, com um indicador booleano `access`. Determina que espaços de cliente o utilizador "
        "pode ver, e é o critério de filtragem da barra lateral.",
    ])
    r.p(
        "A entidade `Permissions` referencia `User` por `email` e não por `id`. Isto é invulgar e é "
        "herdado, não escolhido; funciona porque a coluna é única, mas torna a relação sensível a "
        "alterações de endereço de forma que uma relação por identificador não seria."
    )
    r.p(
        "A entidade `Invitation` é o mecanismo de adesão a uma agência. Um registo guarda um endereço "
        "de correio, a agência de destino, o papel a conceder e um estado. No primeiro início de "
        "sessão, `verifyAndAcceptInvitation` procura um convite pendente correspondente ao endereço "
        "autenticado, cria o registo `User` correspondente, escreve o papel nos metadados do `Clerk` "
        "e elimina o convite. A restrição de unicidade em `Invitation.email` implica que uma pessoa só "
        "pode ter um convite por aceitar em toda a plataforma — restrição aceitável agora e que "
        "precisaria de ser revista se uma pessoa pudesse pertencer a mais do que uma agência."
    )

    r.h(2, "6.3 O modelo de domínio alargado")
    r.p(
        "Os restantes dezassete modelos descrevem as áreas funcionais planeadas. A Figura 4 agrupa-os "
        "por subsistema e assinala o estado atual de cada um."
    )
    r.figure(os.path.join(FIG, "fig5_domain_groups.png"),
             "O modelo de domínio completo agrupado por subsistema, com o estado de implementação. "
             "Os grupos sombreados estão modelados e aguardam implementação.", width_cm=15.5)
    r.p(
        "O grupo de navegação é o exemplo mais nítido de uma área em desenvolvimento. "
        "`AgencySidebarOption` e `SubAccountSidebarOption` guardam o menu lateral como dados e não "
        "como código, para que a navegação possa diferir entre inquilinos. `upsertAgency` cria seis "
        "registos para uma nova agência e `upsertSubAccount` cria oito, a barra lateral carrega-os e "
        "passa-os ao componente de menu; falta o passo de renderização. O caminho dos dados está "
        "completo de ponta a ponta, e é sobre ele que a frente de trabalho atual assenta."
    )
    r.p(
        "Dois pormenores de desenho nos grupos planeados condicionam o trabalho que se lhes segue. "
        "`FunnelPage.content` é uma coluna `LongText` destinada a guardar uma estrutura de página "
        "serializada, que é como um editor visual persiste uma página composta sem exigir uma "
        "alteração de esquema por cada tipo de componente novo. `Lane` e `Ticket` têm ambos uma "
        "coluna inteira `order`, que é a forma habitual de suportar reordenação por arrastamento numa "
        "interface Kanban. Ambas as decisões foram tomadas para não bloquear a implementação futura."
    )

    r.h(2, "6.4 relationMode = \"prisma\" e as suas consequências")
    r.p(
        "O bloco `datasource` define `relationMode = \"prisma\"`. Esta única linha tem sobre a base de "
        "dados um efeito maior do que qualquer outra coisa no esquema, e compreendê-la foi uma das "
        "lições mais valiosas do projeto."
    )
    r.code([
        "datasource db {",
        "  provider     = \"mysql\"",
        "  url          = env(\"DATABASE_URL\")",
        "  relationMode = \"prisma\"",
        "}",
    ], caption="A configuração da datasource que retira a integridade referencial ao `MySQL`.")
    r.p(
        "No modo por omissão, o `Prisma` emite restrições `FOREIGN KEY` e é a base de dados que impõe "
        "a integridade referencial e as eliminações em cascata. Com `relationMode = \"prisma\"` não são "
        "criadas quaisquer restrições: as relações existem apenas no esquema `Prisma` e a integridade "
        "é assegurada pelo cliente, que emite consultas adicionais para emular o comportamento que "
        "uma restrição teria dado. A definição existe para bases de dados alojadas, como o "
        "PlanetScale, que não suportam chaves estrangeiras."
    )
    r.p("As consequências para este projeto são concretas:")
    r.bullets([
        "Cada relação tem de declarar um `@@index` explícito, porque o índice que uma chave "
        "estrangeira criaria implicitamente deixou de existir. O esquema fá-lo de forma consistente "
        "em todos os modelos com relações.",
        "A integridade referencial depende inteiramente do `Prisma`. Uma linha escrita por outra via "
        "— uma instrução SQL manual, um script, uma segunda aplicação — pode criar um órfão que a "
        "base de dados não rejeita.",
        "As eliminações em cascata são emuladas no cliente. As anotações `onDelete: Cascade` do "
        "esquema são respeitadas pelo `Prisma` mas são invisíveis para o `MySQL`.",
        "As ferramentas de engenharia inversa veem uma base de dados sem qualquer relação. Foi assim "
        "que a definição foi descoberta, e a secção 9.6 conta essa história.",
    ])
    r.p(
        "A avaliação a que esta investigação conduziu é que a definição não se justifica nesta "
        "instalação. O projeto usa um servidor `MySQL` local, que suporta chaves estrangeiras sem "
        "qualquer problema, pelo que a restrição que motiva a definição não se aplica aqui. Removê-la "
        "reforça as garantias de integridade sem custo, e está agendada como uma das primeiras "
        "tarefas da secção 13.3. Foi mantida até agora por uma razão de sequência: a alteração deve "
        "ser feita em conjunto com a adoção de um histórico de migrações (secção 6.6), para que a "
        "reintrodução das chaves estrangeiras fique registada numa migração e possa ser aplicada de "
        "forma reproduzível a uma base de dados já povoada."
    )

    r.h(2, "6.5 Evolução do esquema")
    r.p(
        "O esquema foi modificado apenas três vezes desde o primeiro commit, e apenas uma dessas "
        "alterações foi substantiva. O bloco `datasource` ganhou uma atribuição explícita de `url`, a "
        "formatação foi normalizada e o modelo `Agency` perdeu o campo `customerId`."
    )
    r.code([
        " model Agency {",
        "   id               String   @id @default(uuid())",
        "   connectAccountId String?  @default(\"\")",
        "-  customerId       String   @default(\"\")",
        "   name             String",
        "   agencyLogo       String   @db.Text",
    ], caption="A única alteração substantiva ao esquema desde o primeiro commit (commit "
               "\u201cchore(db): remove customerId from Agency model\u201d).")
    r.p(
        "`customerId` era o identificador do registo de cliente da agência no `Stripe`. Como o "
        "`Stripe` não está integrado, o campo nunca poderia ser preenchido com um valor com "
        "significado, e a sua presença no conjunto de campos obrigatórios estava efetivamente a "
        "impedir a criação de agências. Removê-lo é uma alteração pequena com fundamento claro: um "
        "esquema não deve conter um campo obrigatório que nenhum código consegue satisfazer. A secção "
        "9.7 descreve a falha que a motivou."
    )
    r.p(
        "Que o esquema tenha mudado tão pouco é, em si, um resultado. Foi adotado por avaliação e não "
        "por inércia, e três meses de desenvolvimento sobre ele não revelaram necessidade de o "
        "reestruturar: a cadeia de propriedade manteve-se coerente à medida que novas consultas foram "
        "acrescentadas, os índices cobriram todas as relações usadas e as enumerações mantiveram-se "
        "suficientes. A única alteração necessária foi remover um campo que dependia de uma "
        "integração adiada. Um modelo de dados estável sob desenvolvimento incremental é a propriedade "
        "que dele se pretendia."
    )

    r.h(2, "6.6 Estratégia de migrações")
    r.p(
        "O projeto não tem histórico de migrações. Não existe diretório `prisma/migrations` e o "
        "`.gitignore` exclui explicitamente esse caminho. O esquema é aplicado com `prisma db push`, "
        "que reconcilia a base de dados diretamente com o ficheiro de esquema e não regista como a "
        "alteração foi feita."
    )
    r.p(
        "Para desenvolvimento individual contra uma base de dados local este é o fluxo que o próprio "
        "`Prisma` recomenda em fase de prototipagem, e foi adequado enquanto o esquema esteve a ser "
        "estabilizado. Deixa de o ser a partir do momento em que exista uma base de dados que não "
        "possa ser recriada à vontade: sem histórico de migrações não há forma reproduzível de "
        "recriar o esquema de raiz num estado conhecido, nem caminho seguro para aplicar uma "
        "alteração a uma base de dados que já contém dados. Adotar `prisma migrate dev` e gerar uma "
        "migração inicial a partir do esquema atual é a próxima tarefa nesta camada, e está listada "
        "na secção 13.3."
    )
    r.page_break()


capa()
resumo()
pre_textuais()
cap1()
cap2()
cap3()
cap4()
cap5()
cap6()

# a parte 2 é acrescentada por build_report2.py
import build_report2
build_report2.build(r, FIG)

r.add_page_numbers()
path = r.save(OUT)
print("guardado:", path)
print(f"figuras={r.fig_n} tabelas={r.tab_n} listagens={r.lst_n}")
