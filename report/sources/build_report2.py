# -*- coding: utf-8 -*-
"""Relatório Blume, parte 2: capítulos 7 a 14, referências e apêndices."""
import os
from docx.shared import Pt


def build(r, FIG):

    # ======================================================== 7 IMPLEMENTAÇÃO
    r.h(1, "7. Implementação")
    r.p(
        "Este capítulo descreve o que foi construído, subsistema a subsistema. Segue aproximadamente "
        "a ordem por que um utilizador encontra o sistema e não a ordem por que as partes foram "
        "escritas."
    )

    r.h(2, "7.1 Site de divulgação")
    r.p(
        "O ponto de entrada público é `/site`, renderizado como componente de servidor e sem estado "
        "no cliente. Tem uma secção de destaque e uma secção de preços. O destaque usa dois gradientes "
        "CSS sobrepostos para desenhar uma grelha, mascarada com um gradiente radial para esbater nas "
        "margens, por trás do nome do produto preenchido a gradiente. A secção de preços percorre o "
        "vetor `pricingCards` de `src/lib/constants.ts` e produz três planos, cada um com ligação "
        "para `/agency` levando o plano escolhido como parâmetro de consulta."
    )
    r.p(
        "Esse parâmetro é lido pela página de registo, que redirecionaria para uma rota de faturação "
        "se ela existisse. A ligação funciona e o destino não — exemplo de até onde a canalização "
        "para a faturação foi montada antes de a funcionalidade ser retirada do âmbito."
    )
    r.p(
        "O destaque foi também a origem de um problema de layout instrutivo. O fundo em grelha está "
        "posicionado de forma absoluta e cobre a secção, e o título não tinha inicialmente contexto "
        "de empilhamento próprio, pelo que a camada decorativa era pintada por cima do texto. A "
        "correção foi dar aos elementos de texto uma `position` explícita e um `z-index`, em vez de "
        "mexer no fundo. É pouco, mas foi o ponto a partir do qual os contextos de empilhamento em "
        "CSS deixaram de ser matéria de adivinhação."
    )

    r.h(2, "7.2 Autenticação")
    r.p(
        "A autenticação é delegada no `Clerk`. Em vez de usar as páginas alojadas do `Clerk`, o Blume "
        "monta os componentes `<SignIn/>` e `<SignUp/>` em rotas próprias, para que os ecrãs de "
        "autenticação fiquem dentro do layout e do tema da aplicação. Ambas as rotas usam segmentos "
        "catch-all opcionais, `[[...sign-in]]` e `[[...sign-up]]`, porque os fluxos do `Clerk` navegam "
        "para caminhos aninhados em passos como a verificação e a escolha de fator; sem o catch-all, "
        "esses passos devolvem 404."
    )
    r.p(
        "O `ClerkProvider` é montado separadamente no layout de divulgação e no layout autenticado, "
        "ambos configurados com o tema base escuro do `Clerk` para que os componentes acompanhem o "
        "aspeto da aplicação."
    )

    r.h(2, "7.3 Autorização")
    r.p(
        "A autorização é imposta a três níveis, cada um com granularidade diferente. O middleware "
        "decide se o pedido pode sequer prosseguir. O layout da agência decide se o utilizador "
        "autenticado pode entrar na área da agência. Cada server action faz as suas próprias "
        "verificações quando a operação é destrutiva."
    )
    r.code([
        "if (!agencyId) {",
        "  return redirect('/agency')",
        "}",
        "",
        "if (",
        "  user.privateMetadata.role !== \"AGENCY_OWNER\" &&",
        "  user.privateMetadata.role !== \"AGENCY_ADMIN\"",
        ")",
        "  return <Unauthorized/>",
    ], caption="Verificação de papel em `src/app/(main)/agency/[agencyId]/layout.tsx`. Por se tratar "
               "de um componente de servidor, a verificação corre no servidor e o conteúdo protegido "
               "nunca chega a um cliente que não a passe.")
    r.p(
        "O papel é lido de `privateMetadata` do `Clerk` e não da base de dados. Os metadados privados "
        "não são expostos ao browser e só podem ser escritos no servidor, pelo que não se trata do "
        "problema de confiança no cliente que possa parecer à primeira vista. É, ainda assim, "
        "duplicação de estado: o papel existe no registo `User` e no `Clerk`, e nada os mantém "
        "sincronizados se um for alterado sem o outro. A secção 12.3 retoma o ponto."
    )
    r.p(
        "`deleteAgency` é a única ação que volta a derivar a autorização da base de dados em vez de "
        "confiar em quem chama. Resolve o endereço de correio do utilizador autenticado, carrega o "
        "registo `User` correspondente e recusa a operação a menos que esse registo pertença à "
        "agência a eliminar e tenha o papel `AGENCY_OWNER`. Como as server actions ficam alcançáveis "
        "como endpoints depois de a página que as define ter sido servida, esta verificação é a "
        "diferença entre um controlo de autorização e uma convenção de interface."
    )
    r.code([
        "const dbUser = await db.user.findUnique({ where: { email } });",
        "",
        "if (",
        "  !dbUser?.agencyId ||",
        "  dbUser.agencyId !== agencyId ||",
        "  dbUser.role !== 'AGENCY_OWNER'",
        ") {",
        "  throw new Error('Forbidden');",
        "}",
    ], caption="Verificação de posse no servidor, em `deleteAgency` (`src/lib/queries.ts`).")

    r.h(2, "7.4 Registo da agência")
    r.p(
        "A rota `/agency` é o eixo da aplicação. Todos os utilizadores autenticados passam por ela, e "
        "o que acontece a seguir depende de já pertencerem ou não a uma agência. A Figura 5 traça a "
        "sequência completa."
    )
    r.figure(os.path.join(FIG, "fig3_onboarding_flow.png"),
             "Sequência do início de sessão e do registo da agência, desde o pedido inicial até à "
             "aceitação do convite e à criação da agência.", width_cm=16.0)
    r.p(
        "A página começa por chamar `verifyAndAcceptInvitation`, que devolve o identificador de uma "
        "agência se o utilizador já pertencer a uma ou tiver acabado de aceitar um convite. Se vier "
        "um identificador, o utilizador é redirecionado conforme o papel: papéis de subconta para "
        "`/subaccount`, papéis de agência para o painel da agência, exceto se estiver presente um "
        "plano ou um parâmetro de estado OAuth, casos em que estes têm precedência. Se não vier "
        "identificador, é renderizado o formulário de registo."
    )
    r.p(
        "O formulário, `AgencyDetails`, é o componente de cliente mais substancial do projeto. Combina "
        "`react-hook-form` para o estado, um esquema `Zod` para validação, `UploadThing` para o "
        "logótipo, um interruptor para o indicador de marca branca, um campo numérico do `Tremor` "
        "para a meta de crescimento e uma caixa de confirmação para a eliminação. A validação corre "
        "em modo `onChange`, para que os erros surjam à medida que o utilizador escreve."
    )
    r.code([
        "const E164_PHONE_REGEX = /^\\+?[1-9]\\d{1,14}$/",
        "",
        "const requiredString = (requiredError: string) =>",
        "  z.string({ required_error: requiredError }).trim().min(1, requiredError)",
        "",
        "const FormSchema = z.object({",
        "  name: requiredString('Agency name is required.')",
        "    .min(2, 'Agency name must be at least 2 characters long.'),",
        "  companyEmail: requiredString('Company email is required.')",
        "    .email('Invalid email address.'),",
        "  companyPhone: requiredString('Company phone number is required.')",
        "    .regex(E164_PHONE_REGEX, 'Invalid phone number format.'),",
        "  whiteLabel: z.boolean(),",
        "  /* address, city, zipCode, state, country, agencyLogo */",
        "})",
    ], caption="Esquema de validação em `src/components/forms/agency-details.tsx`. O auxiliar "
               "`requiredString` e a regra de telefone E.164 foram acrescentados neste projeto; o "
               "tutorial valida estes campos apenas quanto à presença.")
    r.p(
        "Os campos do formulário estão dentro de um `fieldset` que fica desativado enquanto a promessa "
        "de submissão está pendente, o que impede submissões duplicadas sem necessitar de uma guarda "
        "separada, e o botão de submissão troca a legenda por um indicador de progresso. Ambas são "
        "pequenas decisões de usabilidade tomadas durante o desenvolvimento e não herdadas."
    )
    r.p(
        "A submissão chama `initUser`, que cria ou atualiza o registo `User` e marca quem chama como "
        "`AGENCY_OWNER`, e em seguida `upsertAgency`, que escreve a agência. Em caso de sucesso é "
        "mostrada uma notificação e `router.refresh()` volta a executar o componente de servidor, que "
        "passa a encontrar uma agência e redireciona para o painel."
    )

    r.h(2, "7.5 Semear a navegação do inquilino")
    r.p(
        "`upsertAgency` faz mais do que escrever uma linha. Ao criar uma agência nova, liga-a ao "
        "utilizador com o endereço de correio correspondente e semeia seis registos "
        "`AgencySidebarOption` na mesma operação, para que um inquilino recém-criado tenha uma "
        "estrutura de navegação completa sem uma segunda ida ao servidor. `upsertSubAccount` faz o "
        "equivalente para uma subconta, semeando oito opções de barra lateral e um registo "
        "`Permissions` que dá ao proprietário da agência acesso ao espaço que acabou de criar."
    )
    r.code([
        "SidebarOption: {",
        "  create: [",
        "    { name: \"Dashboard\",    icon: \"category\",      link: `/agency/${agency.id}` },",
        "    { name: \"Sub Accounts\", icon: \"person\",        link: `/agency/${agency.id}/all-subaccounts` },",
        "    { name: \"Team\",         icon: \"shield\",        link: `/agency/${agency.id}/team` },",
        "    { name: \"Launchpad\",    icon: \"clipboardIcon\", link: `/agency/${agency.id}/launchpad` },",
        "    { name: \"Billing\",      icon: \"payment\",       link: `/agency/${agency.id}/billing` },",
        "    { name: \"Settings\",     icon: \"settings\",      link: `/agency/${agency.id}/settings` },",
        "  ],",
        "},",
    ], caption="Criação aninhada da navegação por omissão da agência, dentro de `upsertAgency`. O "
               "`Prisma` escreve a agência e as suas opções de barra lateral numa única operação.")
    r.p(
        "Estes registos são escritos e lidos corretamente, e nenhuma das seis rotas para que apontam "
        "existe. Esta é a ilustração mais clara do estado atual do projeto: a camada de dados vai à "
        "frente da interface."
    )

    r.h(2, "7.6 Convites e membros de equipa")
    r.p(
        "`verifyAndAcceptInvitation` implementa a adesão a uma agência existente. Procura um "
        "`Invitation` com estado `PENDING` correspondente ao endereço autenticado; se existir, chama "
        "`createTeamUser` para inserir o registo `User` com o papel convidado, regista uma notificação "
        "de atividade, copia o papel para os metadados do `Clerk` e elimina o convite. Se não existir "
        "convite, recorre à agência já associada ao utilizador."
    )
    r.p(
        "`createTeamUser` recusa criar um utilizador com o papel `AGENCY_OWNER`, o que é uma guarda "
        "sensata: a posse estabelece-se criando uma agência e não sendo convidado para uma."
    )
    r.p(
        "Há duas limitações a registar em vez de disfarçar. Primeira, não é possível criar convites "
        "pela interface — não existe ecrã de gestão de equipa nem envio de correio eletrónico, pelo "
        "que um registo `Invitation` tem de ser inserido diretamente na base de dados para que o "
        "fluxo possa sequer ser exercitado. Segunda, o código contém um defeito: o nome do novo "
        "utilizador é montado com plicas em vez de template literal, pelo que fica guardado o texto "
        "literal em vez do nome interpolado."
    )
    r.code([
        "// src/lib/queries.ts, dentro de verifyAndAcceptInvitation",
        "name: '${user.firstName} ${user.lastName}',   // guarda o texto literal",
        "",
        "// src/lib/queries.ts, dentro de initUser — forma correta",
        "name: `${user.firstName} ${user.lastName}`,   // guarda o nome interpolado",
    ], caption="Defeito encontrado durante a redação deste relatório: plicas em vez de crases, em "
               "`verifyAndAcceptInvitation`. O `TypeScript` não o consegue detetar porque ambas as "
               "expressões são strings válidas.")
    r.p(
        "Vale a pena reportá-lo por duas razões. É um defeito real que um utilizador veria, e ilustra "
        "bem os limites da tipagem estática: o sistema de tipos verificou que era fornecida uma "
        "string, que é tudo o que pode fazer, e só um teste ou um percurso manual pelo fluxo de "
        "convites teria detetado que era a string errada. Nenhum dos dois existia."
    )

    r.h(2, "7.7 Notificações de atividade")
    r.p(
        "`saveActivityLogsNotification` escreve um registo `Notification` que descreve algo que "
        "aconteceu. Resolve o utilizador responsável a partir da sessão `Clerk` e, quando a "
        "notificação diz respeito a uma subconta, procura essa subconta para descobrir a agência "
        "proprietária, de modo a atribuir a notificação a ambas. É chamada quando uma meta é "
        "alterada, quando uma subconta é guardada e quando um convite é aceite."
    )
    r.p(
        "Uma versão anterior desta função continha uma guarda invertida: todo o corpo estava dentro de "
        "uma verificação que só corria quando quem chamava não estava autenticado, com o efeito de as "
        "notificações nunca serem criadas para utilizadores com sessão iniciada — ou seja, para todos "
        "os chamadores reais. O problema foi notado durante o desenvolvimento, assinalado no código "
        "com um comentário `FIXME` e corrigido reestruturando a função de forma que os caminhos "
        "autenticado e não autenticado resolvam cada um o seu utilizador e a escrita partilhada "
        "aconteça depois. A implementação atual está correta."
    )
    r.p(
        "As notificações são guardadas e podem ser consultadas — `getNotifications` lê-as para uma "
        "agência, das mais recentes para as mais antigas, e o layout da agência chama-a. O resultado é "
        "atribuído a uma variável que nunca é usada, e o `ESLint` assinala-o. Não existe interface de "
        "notificações."
    )

    r.h(2, "7.8 Carregamento de ficheiros")
    r.p(
        "Os carregamentos seguem o modelo de file router do `UploadThing`. O servidor declara rotas "
        "nomeadas com as suas restrições e um middleware de autenticação; o cliente usa componentes "
        "gerados e ligados ao tipo do router, pelo que um erro de escrita no nome de uma rota é um "
        "erro de compilação e não uma falha em execução."
    )
    r.code([
        "export const ourFileRouter = {",
        "  agencyLogo: f({",
        "    image: { maxFileSize: LOGO_ROUTE_MAX_FILE_SIZE, maxFileCount: 1 },",
        "  })",
        "    .middleware(authenticateUser)",
        "    .onUploadComplete(() => {}),",
        "  /* subaccountLogo, avatar, media declaradas de forma idêntica */",
        "} satisfies FileRouter;",
        "",
        "export type OurFileRouter = typeof ourFileRouter;",
    ], caption="O file router do `UploadThing` em `src/app/api/uploadthing/core.ts`.")
    r.p(
        "O limite de tamanho é definido uma única vez em `src/lib/uploadthing-limits.ts` e importado "
        "tanto pela rota do servidor como pelo componente de cliente que mostra o limite ao "
        "utilizador, pelo que os dois não podem divergir. Este pequeno módulo foi escrito para este "
        "projeto."
    )
    r.p(
        "O invólucro do cliente, `FileUpload`, trata do caso que causou o problema mais visível na "
        "prática. Os logótipos carregados pelos utilizadores têm dimensões arbitrárias, e a "
        "pré-visualização de tamanho fixo do tutorial deixava as imagens altas transbordar para fora "
        "do layout envolvente. O componente renderiza agora as pré-visualizações dentro de um "
        "contentor `AspectRatio` de 16:5 com `object-contain`, e apresenta um tamanho recomendado ao "
        "lado da zona de largada. A secção 9.9 descreve a correção correspondente na barra lateral."
    )
    r.p(
        "Deve registar-se uma fragilidade. O middleware de carregamento verifica que quem chama está "
        "autenticado mas não associa o carregamento a um inquilino, e `onUploadComplete` não faz nada. "
        "Os ficheiros carregados não pertencem, por isso, a nada até que uma submissão de formulário "
        "guarde o URL devolvido num registo, e qualquer utilizador autenticado da plataforma pode "
        "carregar por qualquer rota."
    )

    r.h(2, "7.9 Estrutura base da aplicação")
    r.p(
        "A área autenticada é enquadrada por uma barra lateral. A sua metade de servidor, `Sidebar`, "
        "carrega o utilizador com a sua agência, subcontas, permissões e opções de barra lateral, "
        "escolhe o logótipo a mostrar segundo a regra de marca branca e filtra a lista de subcontas "
        "para as que o utilizador pode ver. A metade de cliente, `MenuOptions`, renderiza o resultado."
    )
    r.p(
        "A barra fixa em ambiente de secretária e a gaveta em dispositivos móveis são o mesmo "
        "componente renderizado duas vezes com propriedades diferentes: uma forçada permanentemente "
        "aberta e escondida abaixo do ponto de rutura médio, a outra deixada não controlada e "
        "escondida acima dele. Isto evita duplicar o conteúdo da barra lateral, ao custo de renderizar "
        "as duas instâncias no DOM."
    )
    r.p(
        "As janelas modais são geridas por um pequeno contexto React, `ModalProvider`, que guarda a "
        "modal em exibição, um indicador de abertura e um objeto de dados partilhado. O seu `setOpen` "
        "aceita um carregador assíncrono opcional cujo resultado é fundido no contexto antes de a "
        "modal ser mostrada, pelo que uma caixa pode ser aberta e preenchida numa só chamada. É este "
        "o mecanismo pelo qual o seletor de conta abre o formulário de criação de subconta."
    )

    r.h(2, "7.10 Criação de subcontas")
    r.p(
        "`SubAccountDetails` espelha `AgencyDetails` na estrutura: a mesma abordagem de validação, o "
        "mesmo componente de carregamento apontado à rota `subaccountLogo`, o mesmo padrão de "
        "`fieldset` desativado durante a submissão. Ao submeter, chama `upsertSubAccount`, regista uma "
        "notificação de atividade, fecha a modal e atualiza a rota."
    )
    r.p(
        "A subconta é criada corretamente, com as permissões e a navegação semeadas. Passa então a "
        "aparecer no seletor de conta, com ligação para uma rota que não existe."
    )

    r.h(2, "7.11 O que não está implementado")
    r.p(
        "Para que não restem dúvidas, o seguinte está completamente ausente do código: qualquer "
        "interface ou consulta de CRM; qualquer editor de funis, renderizador de funis ou mecanismo "
        "de publicação; qualquer biblioteca de multimédia; qualquer execução de automações; qualquer "
        "integração com o `Stripe` — o SDK não está instalado e os únicos vestígios são variáveis de "
        "ambiente, uma entrada de host de imagens e três comentários no código; qualquer interface de "
        "gestão de equipa; qualquer área de subconta; e qualquer teste automatizado."
    )
    r.page_break()

    # ======================================================== 8 PROCESSO
    r.h(1, "8. Processo de Desenvolvimento")

    r.h(2, "8.1 Abordagem")
    r.p(
        "O projeto foi desenvolvido por uma só pessoa em paralelo com as unidades curriculares, em "
        "sessões que variaram entre vinte minutos e um dia inteiro. Não foi adotada nenhuma "
        "metodologia formal, e seria desonesto descrever o processo como Scrum ou Kanban a "
        "posteriori. O que realmente aconteceu descreve-se melhor como desenvolvimento incremental "
        "guiado por tutorial, e passou por três fases visíveis tanto no diário como no histórico de "
        "commits."
    )
    r.p(
        "Na primeira fase o tutorial foi seguido de perto, com o esforço concentrado em pôr o "
        "ambiente e a camada de autenticação a funcionar. Na segunda fase o tutorial continuou a ser "
        "a fonte da sequência de funcionalidades, mas a maioria das sessões consistiu em traduzir as "
        "suas instruções para APIs que tinham mudado. Na terceira fase, a partir do trabalho na barra "
        "lateral, o tutorial passou a ser referência de intenção e não fonte de código, porque tinha "
        "começado a avançar mais depressa do que explicava e o trabalho passou cada vez mais a ser "
        "reproduzir um comportamento e não uma listagem."
    )

    r.h(2, "8.2 Controlo de versões")
    r.p(
        "O repositório contém 73 commits num único ramo, entre junho de 2025 e agosto de 2026. A "
        "Figura 6 mostra como esse trabalho se distribuiu de forma desigual."
    )
    r.figure(os.path.join(FIG, "fig6_commits.png"),
             "Commits por mês. Quatro commits antecedem maio de 2026; os restantes 69 concentram-se "
             "num período de quatro meses.", width_cm=14.5)
    r.p(
        "A distribuição é honesta quanto ao modo como o projeto decorreu. Três commits de 2025 "
        "correspondem à configuração inicial e às primeiras tentativas no middleware, seguidos de um "
        "período dormente interrompido apenas por um commit em abril de 2026. O desenvolvimento "
        "sustentado começou em maio de 2026 e prolongou-se por quatro meses, com uma pausa de duas "
        "semanas em julho que o diário atribui a um período de baixa motivação. Reportar isto é mais "
        "útil do que apresentar uma cronologia idealizada, porque o padrão — longa paragem seguida de "
        "recuperação concentrada — é comum e instrutivo em projetos individuais de estudante."
    )
    r.p(
        "A higiene dos commits melhorou ao longo do projeto. Apenas o primeiro commit não tem prefixo "
        "convencional e, a partir de abril de 2026, as mensagens tornam-se consistentemente "
        "imperativas e de âmbito estreito, com um tipo, um âmbito opcional e um resumo curto. Não foi "
        "disciplina espontânea: foi escrito um comando reutilizável que instrui o assistente do "
        "editor a analisar a árvore de trabalho, agrupar alterações por assunto e propor um plano de "
        "commits antes de preparar o que quer que seja. Adotá-lo mudou tanto a granularidade do "
        "histórico como a redação, substituindo commits grandes e mistos por outros pequenos, como "
        "\u201cfix(sidebar): contain logo inside AspectRatio box\u201d."
    )

    r.h(2, "8.3 Recurso a assistência por IA")
    r.p(
        "Foram usados assistentes de IA ao longo do projeto, e o relatório ficaria incompleto se não "
        "o dissesse e não caracterizasse esse uso com rigor. Foram usados de quatro formas distintas, "
        "com valor muito diferente."
    )
    r.bullets([
        "**Como leitor de documentação.** O uso mais valioso. Dadas as secções relevantes da "
        "documentação do `Clerk` e uma descrição da falha, um assistente ajudou a reduzir um ciclo de "
        "redireções a uma configuração concreta de matcher muito mais depressa do que a leitura "
        "isolada teria permitido.",
        "**Como gerador de código.** Usado em campos repetitivos de formulário e em esqueletos de "
        "componentes, onde o resultado podia ser confrontado com um exemplo já funcional.",
        "**Como auxiliar de refactorização.** Usado para reestruturar código com muitos níveis de "
        "aninhamento; foi assim que o auxiliar privado `getUser` em `queries.ts` passou a existir.",
        "**Como agente autónomo.** O uso menos fiável. As alterações conduzidas por agente tiveram "
        "frequentemente de ser revistas e parcialmente revertidas, sobretudo quando um agente "
        "introduziu um ficheiro de bloqueio do `npm` num projeto `Bun` e quando apagou código que "
        "estava intencionalmente presente.",
    ])
    r.p(
        "O padrão que emergiu não é surpreendente mas vale a pena enunciar: a assistência foi mais "
        "útil quando o problema estava bem especificado e o resultado era verificável, e menos útil "
        "quando lhe foi dada margem para decidir o que alterar. O diário regista várias sessões "
        "gastas a rever e reverter alterações geradas e, pelo menos num problema — a falha na criação "
        "de agências da secção 9.7 —, o assistente produziu um resultado funcional cujo raciocínio "
        "teve de ser reconstruído depois, revertendo deliberadamente para a versão do tutorial e "
        "reproduzindo a falha. É esse passo de reconstrução que vale a pena manter no processo."
    )

    r.h(2, "8.4 Divergência face ao tutorial")
    r.p(
        "A Tabela 6 regista concretamente onde o sistema entregue difere do seu ponto de partida. É a "
        "evidência que suporta a afirmação da secção 2.4 de que o projeto não é original na "
        "arquitetura nem é uma transcrição."
    )
    r.table(
        ["Área", "Tutorial", "Blume", "Porquê"],
        [
            ["Versão da framework", "`Next.js 14` / `React 18` à data da gravação",
             "`Next.js 14.2.24`, fixada deliberadamente",
             "O `Next.js 15` com `React 19` quebrava a instalação de componentes; a versão 14 foi escolhida após testes"],
            ["Middleware do Clerk", "Uma API de middleware anterior",
             "`clerkMiddleware` com `createRouteMatcher` e padrões `(.*)`",
             "A API usada pelo tutorial já tinha sido substituída quando o projeto começou"],
            ["Import do cliente Prisma", "`@prisma/client`",
             "`src/generated/prisma`",
             "O esquema gera para um caminho próprio; o import por omissão resolve para o cliente errado"],
            ["Versões do Prisma", "Não fixadas",
             "`prisma` e `@prisma/client` fixados em 6.9.0 via `overrides`",
             "A divergência de versões entre os dois pacotes quebrava a geração do cliente"],
            ["`Agency.customerId`", "Campo obrigatório preenchido pelo `Stripe`",
             "Campo removido do esquema",
             "O `Stripe` não está integrado, pelo que o campo nunca poderia ter um valor válido"],
            ["Stripe", "Integrado",
             "Não integrado; permanecem modelos e variáveis de ambiente",
             "Retirado do âmbito deliberadamente"],
            ["Validação de formulários", "Verificação de presença",
             "Auxiliares `Zod` reutilizáveis, validação E.164 de telefone, mensagens por campo",
             "Decisão independente para melhorar a qualidade dos dados"],
            ["Reposição do formulário", "`form.reset(data)`",
             "`reset` com `...form.getValues()` antes de `...data`",
             "Uma reposição simples limpava o campo booleano de marca branca (secção 9.8)"],
            ["Eliminação de agência", "Não presente no ponto atingido",
             "`deleteAgency` com verificação de posse no servidor e caixa de confirmação",
             "Acrescentado de forma independente"],
            ["Tratamento do logótipo", "Pré-visualização de tamanho fixo, imagens escolhidas",
             "Contentor `AspectRatio` 16:5, `object-contain`, sugestão de tamanho",
             "Imagens de utilizador com dimensões arbitrárias quebravam o layout"],
            ["Componente `Sheet`", "Componente `shadcn/ui` original",
             "Estendido com uma propriedade `showX`",
             "A barra fixa de secretária não deve mostrar botão de fecho"],
            ["Limites de carregamento", "Literais em linha",
             "Constante única partilhada, importada pelo servidor e pelo cliente",
             "Impede que o limite mostrado e o limite imposto divirjam"],
        ],
        "Onde o sistema entregue diverge do tutorial de que partiu.",
        widths=[3.0, 4.0, 4.6, 5.0], font_size=8.2,
    )

    r.h(2, "8.5 Orientação")
    r.p(
        "O contributo do orientador moldou o projeto num ponto identificável. Após a primeira reunião, "
        "o orientador pediu um diagrama entidade-relação obtido por engenharia inversa da base de "
        "dados com o MySQL Workbench. A tentativa produziu um diagrama de tabelas desligadas, o que "
        "parecia um erro e veio a revelar-se uma representação exata do que a base de dados realmente "
        "continha. Investigar porquê foi o que conduziu a uma compreensão adequada de "
        "`relationMode = \"prisma\"` (secção 9.6). Um pedido de documentação de rotina produziu, "
        "assim, a aprendizagem mais útil de todo o projeto sobre a camada de persistência."
    )
    r.page_break()

    # ======================================================== 9 PROBLEMAS
    r.h(1, "9. Problemas Técnicos e Resolução")
    r.p(
        "Este capítulo analisa os problemas que alteraram a forma do projeto. Erros de rotina — "
        "imports em falta, erros de tipos, ajustes de estilo — foram omitidos. Cada caso é "
        "apresentado como o problema observado, o que foi investigado, o que foi decidido e porquê, o "
        "que resultou e o que ensinou."
    )

    r.h(2, "9.1 Conflito de versões logo no início")
    r.p("**Problema.** No primeiro dia de trabalho, instalar o conjunto de componentes `shadcn/ui` "
        "num projeto `Next.js` acabado de criar falhou. O instalador reportou conflitos de "
        "dependências de pares e propôs forçar a instalação ou recorrer à resolução antiga.")
    r.p("**Investigação.** O `Next.js 15`, então recém-lançado, depende do `React 19`. Vários pacotes "
        "de componentes do ecossistema `shadcn/ui` declaravam ainda intervalos de pares para o "
        "`React 18`, pelo que o grafo de dependências não podia ser satisfeito de forma limpa. Forçar "
        "a instalação produziria uma árvore que resolvia mas sem garantia de comportamento, e o "
        "tutorial que estava a ser seguido tinha, de qualquer modo, sido gravado sobre o `React 18`.")
    r.p("**Decisão.** O projeto foi recriado sobre `Next.js 14` com `React 18`. O raciocínio foi que "
        "gastar as primeiras semanas de um projeto final a depurar incompatibilidades ao nível do "
        "ecossistema consumiria tempo que tinha de ir para os problemas do próprio projeto, e que ter "
        "um tutorial e uma árvore de dependências coerentes entre si vale mais, no início, do que "
        "estar na versão mais recente.")
    r.p("**Resultado.** A instalação passou a funcionar e o projeto manteve-se em `Next.js 14` desde "
        "então. Seguiu-se pouco depois um segundo recomeço por razão distinta — o projeto tinha sido "
        "gerado sem o diretório `src` que o tutorial pressupunha — e a configuração foi reconstruída "
        "de raiz em vez de remendada.")
    r.p("**Lição.** Escolher versões é uma decisão de desenho com consequências e não um pormenor. "
        "Corta também nos dois sentidos: a mesma decisão que removeu atrito no primeiro dia é a razão "
        "pela qual o projeto está hoje duas versões maiores atrasado, o que fica registado como "
        "dívida técnica na secção 13.2.")

    r.h(2, "9.2 HTTP 431 e um ciclo de redireções no middleware")
    r.p("**Problema.** Pedir a página de início de sessão produzia uma resposta HTTP 431, "
        "\u201cRequest Header Fields Too Large\u201d, e o componente de sessão do `Clerk` nunca "
        "chegava a ser renderizado. Isto bloqueou o projeto durante cerca de uma semana de sessões de "
        "trabalho e é o maior obstáculo isolado de toda a história de desenvolvimento.")
    r.p("**Investigação.** O 431 era um sintoma e não a falha. Algo levava o servidor a redirecionar "
        "repetidamente, e cada salto acumulava estado nos cabeçalhos do pedido até o bloco de "
        "cabeçalhos exceder o limite do servidor. A pergunta certa era, portanto, o que estava a "
        "redirecionar e não porque eram os cabeçalhos grandes. Ler com atenção a documentação do "
        "middleware do `Clerk`, a par de relatos de falhas semelhantes de outros programadores, "
        "isolou a causa: a lista de rotas públicas do middleware correspondia exatamente a "
        "`/agency/sign-in`. O fluxo de início de sessão do `Clerk` não permanece nesse caminho — "
        "navega para caminhos aninhados para a verificação e outros passos. Esses caminhos aninhados "
        "não correspondiam ao padrão de rota pública, pelo que o middleware os tratava como "
        "protegidos e os redirecionava para a página de início de sessão, que navegava para um "
        "caminho aninhado, que era novamente redirecionado.")
    r.p("**Decisão e implementação.** Os padrões foram alterados para incluir um sufixo de expressão "
        "regular, de modo que toda a subárvore abaixo de cada rota de autenticação seja pública:")
    r.code([
        "const isPublicRoute = createRouteMatcher([",
        "  '/site',",
        "  '/agency/sign-in(.*)',    // (.*) abrange cada passo aninhado do fluxo",
        "  '/agency/sign-up(.*)',",
        "  '/api/uploadthing',",
        "]);",
    ])
    r.p("**Resultado.** O ciclo parou de imediato e o componente passou a renderizar corretamente. O "
        "padrão mantém-se inalterado no middleware atual.")
    r.p("**Lição.** Duas, sendo a segunda a mais útil. Primeira, um código de erro pode estar vários "
        "passos afastado da sua causa; tratar o 431 como um problema de dimensão de cabeçalhos não "
        "levaria a lado nenhum. Segunda, um matcher de rotas descreve um conjunto de URL, e raciocinar "
        "sobre ele exige saber que URL a framework ou a biblioteca vão efetivamente gerar — o que "
        "implicou ler a documentação do fluxo de autenticação e não a do middleware.")

    r.h(2, "9.3 Duas implementações concorrentes de middleware")
    r.p("**Problema.** Depois de resolvido o ciclo de redireções, a redireção continuava errada de "
        "forma mais subtil: um utilizador que iniciasse sessão com sucesso era devolvido a `/site` em "
        "vez de `/agency`. As tentativas de correção produziram uma segunda implementação de "
        "middleware a par da primeira e, durante um período, o repositório continha ambas, uma delas "
        "renomeada para `true_middleware.ts`.")
    r.p("**Investigação.** A segunda implementação tinha sido adaptada de uma cópia do repositório do "
        "tutorial encontrada no GitHub, escrita sobre a API antiga do `Clerk`. Em vez de substituir o "
        "middleware funcional, introduziu um conjunto diferente de falhas e, com dois ficheiros em "
        "jogo, tornou-se difícil atribuir qualquer comportamento a um deles.")
    r.p("**Decisão.** A versão adaptada foi abandonada e a implementação funcional restaurada como "
        "middleware único, sendo depois estendida no lugar com o comportamento em falta: redireções "
        "explícitas para utilizadores autenticados que peçam as páginas de autenticação, e "
        "normalização dos caminhos `/sign-in` e `/sign-up` sem âmbito para os equivalentes com âmbito "
        "de agência.")
    r.p("**Resultado.** A redireção após autenticação passou a comportar-se corretamente, e o ficheiro "
        "que sobreviveu é o que hoje está no repositório.")
    r.p("**Lição.** Manter duas implementações do mesmo ponto de controlo custa mais do que qualquer "
        "das correções vale, porque todas as observações passam a ser ambíguas. A lição associada é "
        "sobre portabilidade: código escrito para outra versão maior de uma dependência é muitas "
        "vezes mais caro de adaptar do que de reescrever a partir da documentação atual.")

    r.h(2, "9.4 Onde vive realmente o cliente Prisma")
    r.p("**Problema.** Os imports de tipos de modelo a partir de `@prisma/client`, como escritos no "
        "tutorial, não resolviam, ao passo que os mesmos tipos importados de um diretório gerado "
        "dentro de `src` funcionavam. Não era óbvio qual estava correto e, durante um período, as "
        "duas formas coexistiram no código.")
    r.p("**Investigação.** O bloco `generator` do esquema define um caminho de saída explícito:")
    r.code([
        "generator client {",
        "  provider = \"prisma-client-js\"",
        "  output   = \"../src/generated/prisma\"",
        "}",
    ])
    r.p("Com um caminho de saída definido, o cliente é emitido aí em vez de em `node_modules`, e o "
        "pacote `@prisma/client` deixa de reexportar os tipos gerados do projeto. Os dois caminhos de "
        "import não eram, portanto, equivalentes: um referia-se ao cliente gerado a partir deste "
        "esquema e o outro a um pacote que nada sabia sobre ele.")
    r.p("**Decisão.** O caminho gerado foi adotado de forma consistente, confirmado contra a "
        "documentação do `Prisma` sobre localizações de saída personalizadas. Um problema relacionado "
        "foi resolvido em simultâneo: versões desencontradas entre `prisma` e `@prisma/client` "
        "causavam falhas de geração, pelo que ambos foram fixados em 6.9.0 através de `overrides` no "
        "`package.json`.")
    r.p("**Resultado.** Os imports resolvem de forma consistente e a verificação de tipos passa. O "
        "diretório gerado está excluído do controlo de versões, razão pela qual o `README` instrui "
        "quem clona o repositório a executar `prisma generate`.")
    r.p("**Lição.** Código gerado é um artefacto de compilação com uma localização, e essa localização "
        "é configuração. O ponto mais geral é que, quando os imports de um tutorial falham, a "
        "diferença está muitas vezes na configuração e não no código importado.")

    r.h(2, "9.5 Registos que pareciam não produzir nada")
    r.p("**Problema.** Um `console.log` na página `/agency` não produzia qualquer saída na consola do "
        "browser, o que foi lido como prova de que o código não estava a correr e conduziu a tempo "
        "gasto a depurar uma redireção que, na verdade, funcionava corretamente.")
    r.p("**Investigação e resultado.** A página é um React Server Component. O seu corpo executa no "
        "servidor, pelo que a saída aparece no terminal que corre o servidor de desenvolvimento e "
        "nunca chega ao browser. O registo esteve lá o tempo todo, na outra janela.")
    r.p("**Lição.** É um erro pequeno com uma lição desproporcionada, e é por isso que fica incluído. "
        "A separação servidor/cliente no App Router não é um pormenor de como o código é empacotado; "
        "determina onde o código corre, onde os seus efeitos são observáveis e, portanto, como pode "
        "sequer ser depurado. Compreender isto mudou a forma como o resto do projeto foi abordado.")

    r.h(2, "9.6 Uma base de dados sem relações")
    r.p("**Problema.** Pedido pelo orientador um diagrama entidade-relação, a abordagem habitual — "
        "engenharia inversa da base de dados com o MySQL Workbench — produziu um diagrama com todas "
        "as tabelas e nenhuma das relações entre elas.")
    r.p("**Investigação.** A primeira hipótese, de que a ferramenta tinha sido mal usada, estava "
        "errada. O Workbench deriva as relações das restrições de chave estrangeira, e a inspeção "
        "mostrou que a base de dados genuinamente não tinha nenhuma. Seguir o rasto na documentação "
        "do `Prisma` identificou a causa: `relationMode = \"prisma\"` instrui o `Prisma` a não emitir "
        "chaves estrangeiras e a impor a integridade referencial no cliente. O diagrama estava "
        "correto. A base de dados não tinha mesmo relações, por configuração.")
    r.p("**Decisão.** A definição foi mantida, porque o esquema já declarava o `@@index` compensatório "
        "em todas as relações e alterá-la contra uma base de dados povoada não se justificava naquela "
        "fase. Para o diagrama em si, mudou-se a fonte de verdade: em vez de engenharia inversa da "
        "base de dados, o diagrama passou a ser gerado a partir do esquema `Prisma`, que contém as "
        "relações.")
    r.p("**Resultado.** Foi produzido um diagrama correto e o projeto ganhou uma compreensão rigorosa "
        "de onde reside efetivamente a sua integridade referencial. A secção 6.4 regista as "
        "consequências e a secção 13.3 recomenda remover a definição.")
    r.p("**Lição.** A lição isolada mais valiosa do projeto. Um ORM não é uma janela transparente "
        "sobre uma base de dados; é uma camada com configuração própria, e essa configuração pode "
        "mudar o que a base de dados é. Um ficheiro de esquema que mostra relações e uma base de "
        "dados que não tem nenhuma são ambos descrições exatas de coisas diferentes, e saber que "
        "garantias são impostas onde é a diferença entre presumir integridade e tê-la.")

    r.h(2, "9.7 Criação de agências bloqueada por uma dependência não implementada")
    r.p("**Problema.** Submeter o formulário de criação de agência não criava a agência. Não surgia "
        "qualquer erro na interface; a submissão simplesmente não tinha efeito.")
    r.p("**Investigação.** O handler de submissão do tutorial cria um cliente no `Stripe`, guarda o "
        "identificador devolvido numa variável local e protege a escrita com uma verificação que "
        "retorna cedo quando não há identificador de cliente disponível. Como o `Stripe` nunca foi "
        "integrado, essa variável era sempre `undefined`, pelo que a guarda retornava antes da "
        "escrita em todas as submissões. O problema era agravado pelo esquema: `Agency.customerId` "
        "era um campo não anulável, pelo que o tipo `Agency` gerado exigia um valor em todas as "
        "escritas e o formulário tinha de fornecer um marcador para algo sem significado.")
    r.p("**Decisão e implementação.** Em vez de aceitar uma correção sem a compreender, a versão do "
        "tutorial foi deliberadamente restaurada e a falha reproduzida, para confirmar qual das três "
        "causas candidatas — a guarda, o efeito que repõe o formulário ou o campo em falta — era a "
        "responsável. Confirmada a causa, foram feitas três alterações: a guarda e o bloco de criação "
        "de cliente foram removidos do caminho de submissão, o argumento `customerId` foi comentado "
        "com uma nota a explicar porquê, e `customerId` foi eliminado do modelo `Agency`.")
    r.p("**Resultado.** A criação de agências funciona. A linha comentada e o comentário `WIP` "
        "permanecem no código como marcador do ponto onde o `Stripe` se ligaria.")
    r.p("**Lição.** Retirar uma funcionalidade do âmbito não é gratuito: os seus vestígios persistem "
        "em guardas, campos obrigatórios e fluxo de controlo, e falham silenciosamente. O ponto "
        "metodológico importa mais do que a correção — reverter para o estado avariado para confirmar "
        "um diagnóstico, em vez de aceitar uma alteração que fez o sintoma desaparecer, é a diferença "
        "entre compreender um sistema e limitar-se a operá-lo.")

    r.h(2, "9.8 Uma reposição de formulário que apagava um campo")
    r.p("**Problema.** O interruptor de marca branca comportava-se de forma inconsistente e o `Zod` "
        "rejeitava o formulário com um erro de tipo num campo booleano, reportando como em falta um "
        "valor obrigatório quando o utilizador nem sequer tinha tocado no interruptor.")
    r.p("**Investigação.** O componente preenche o formulário a partir de uma propriedade `data` "
        "dentro de um efeito, usando `form.reset(data)`. O `reset` do `react-hook-form` substitui "
        "todo o estado do formulário pelo objeto que recebe. A propriedade é um `Partial<Agency>` — no "
        "caminho de criação contém apenas o endereço de correio — pelo que repor a partir dela "
        "descartava todos os outros campos, incluindo `whiteLabel`, que ficava `undefined`. O esquema "
        "declara `z.boolean()`, e `undefined` não é um booleano.")
    r.p("**Decisão.** Fundir em vez de substituir, para que os valores recebidos sobreponham os atuais "
        "e as chaves ausentes os deixem intactos:")
    r.code([
        "useEffect(() => {",
        "  if (data) {",
        "    // Merge over current values since `data` may be partial;",
        "    // a plain reset(data) would clear other fields and the `whiteLabel`",
        "    // boolean, breaking z.boolean().",
        "    form.reset({ ...form.getValues(), ...data });",
        "  }",
        "}, [data]);",
    ])
    r.p("**Resultado.** Tanto o caminho de criação como o de edição se comportam corretamente, e o "
        "mesmo padrão foi aplicado ao formulário de subconta.")
    r.p("**Lição.** Um tipo parcial numa assinatura é uma afirmação sobre o que pode estar ausente, e "
        "o código que o consome tem de ser escrito para isso. O erro não estava no esquema de "
        "validação, que estava correto, mas na gestão de estado, que violava os pressupostos do "
        "esquema antes de a validação sequer correr.")

    r.h(2, "9.9 Uma barra lateral, duas apresentações")
    r.p("**Problema.** A barra lateral produziu um conjunto de defeitos relacionados: o botão de menu "
        "em dispositivos móveis não abria a gaveta; logótipos de agência com dimensões arbitrárias "
        "transbordavam e cobriam os controlos por baixo; e o seletor de conta era desenhado por cima "
        "das modais abertas a partir dele, enquanto o botão de menu era desenhado por cima da camada "
        "de sobreposição da modal.")
    r.p("**Investigação.** Todos remontavam à mesma decisão de desenho. Para evitar duplicar o "
        "conteúdo da barra lateral, um único componente é renderizado duas vezes: uma forçada "
        "permanentemente aberta como barra fixa de secretária, outra não controlada como gaveta "
        "móvel. Forçar a propriedade de abertura em ambas as instâncias tornava a gaveta móvel "
        "incontrolável. O problema de layout tinha outra origem: o tutorial usava logótipos "
        "escolhidos e de tamanho consistente, ao passo que utilizadores reais carregam imagens de "
        "proporção arbitrária, e um contentor de altura fixa não as consegue acomodar. Os problemas "
        "de empilhamento vinham de a moldura da barra lateral e as primitivas de diálogo terem "
        "recebido valores de `z-index` sem uma ordenação partilhada.")
    r.p("**Decisão e implementação.** A propriedade de abertura passou a ser aplicada apenas à "
        "instância de secretária, para que a gaveta móvel gira o seu próprio estado. O logótipo passou "
        "a estar dentro de um contentor `AspectRatio` fixo de 16:5 com `object-contain`, de modo que "
        "qualquer imagem se ajusta em vez de transbordar, e o componente de carregamento passou a "
        "sugerir um tamanho recomendado. Foi estabelecida uma ordem de empilhamento coerente entre a "
        "barra lateral, o popover e o diálogo, e o botão de menu é escondido enquanto houver uma "
        "modal global aberta. O componente `Sheet` do `shadcn/ui` foi estendido com uma propriedade "
        "`showX`, para que a barra de secretária possa omitir um controlo de fecho de que a gaveta "
        "móvel precisa.")
    r.p("**Resultado.** Sete commits sucessivos em agosto de 2026 resolveram estes problemas, e a "
        "barra lateral comporta-se corretamente em ambos os pontos de rutura.")
    r.p("**Lição.** Partilhar um componente entre duas apresentações muito diferentes é económico mas "
        "concentra a complexidade nas suas propriedades, e cada propriedade que significa algo "
        "diferente em cada instância é um sítio por onde as duas podem divergir. A lição mais ampla "
        "diz respeito aos dados de teste: os recursos escolhidos de um tutorial escondem uma classe "
        "inteira de problemas de layout que aparece de imediato com dados reais de utilizador, o que "
        "é razão para testar cedo com dados incómodos em vez de convenientes.")
    r.page_break()

    # ======================================================== 10 TESTES
    r.h(1, "10. Testes e Validação")
    r.p(
        "Este capítulo reporta apenas o que foi efetivamente feito. Não foram escritos testes "
        "automatizados, não foi medida cobertura e não foi corrido qualquer teste de desempenho; "
        "onde uma forma de validação esteve ausente, isso é declarado e não substituído."
    )

    r.h(2, "10.1 Abordagem")
    r.p(
        "A validação assentou em três práticas: análise estática pelo compilador de `TypeScript` e "
        "pelo `ESLint`, testes manuais exploratórios no browser após cada alteração, e inspeção "
        "direta da base de dados com o MySQL Workbench para confirmar que as operações produziam os "
        "registos esperados. É um regime pobre, e a secção 10.4 é explícita quanto ao que ele não "
        "consegue detetar."
    )

    r.h(2, "10.2 Análise estática")
    r.p(
        "Foram executadas duas verificações sobre o repositório no seu estado atual durante a "
        "preparação deste relatório. Os resultados são reportados como medidos, incluindo o que falha."
    )
    r.table(
        ["Verificação", "Comando", "Resultado"],
        [
            ["Verificação de tipos", "`bunx tsc --noEmit`",
             ("Passa sem erros", True)],
            ["Compilação Webpack", "parte de `next build`",
             ("Compila com sucesso", True)],
            ["ESLint (código da aplicação)", "`bun run lint`",
             ("16 erros e 2 avisos em 7 ficheiros", True)],
            ["ESLint (cliente Prisma gerado)", "`bun run lint`",
             ("Vários milhares de erros; o diretório não está excluído", True)],
            ["Build de produção", "`bun run build`",
             ("Falha na fase de lint, depois de compilar com sucesso", True)],
            ["Testes automatizados", "\u2014",
             ("Nenhum; não há framework de testes instalada", True)],
        ],
        "Resultados de análise estática e de compilação, medidos sobre o estado atual do repositório.",
        widths=[5.0, 4.4, 7.2], font_size=8.5,
    )
    r.p(
        "A falha de compilação merece ser reportada de forma direta e não escondida. O `next build` "
        "corre o `ESLint` como barreira depois da compilação, e falha. A maioria dos erros vem de "
        "`src/generated/prisma`, que é código gerado por máquina e nunca deveria ter sido analisado; "
        "como o esquema gera o cliente para dentro de `src`, este cai no âmbito por omissão do linter "
        "e não foi acrescentada nenhuma entrada de exclusão. Os restantes erros são genuínos e "
        "informativos:"
    )
    r.bullets([
        "uma variável `allNotifications` não usada no layout da agência, que é a funcionalidade de "
        "notificações a parar um passo antes da interface;",
        "variáveis `custId` e `bodyData` não usadas no formulário da agência, que são o resíduo da "
        "integração `Stripe` removida;",
        "uma propriedade `sidebarOptions` não usada no componente de menu, que é a navegação não "
        "renderizada;",
        "tipos `any` explícitos nas propriedades da barra lateral e no layout da agência;",
        "um tipo de objeto vazio usado como tipo de propriedades em dois componentes.",
    ])
    r.p(
        "Por outras palavras, o linter aponta para as mesmas costuras incompletas que este relatório "
        "identifica noutros pontos, o que é argumento razoável para o tratar como barreira e não como "
        "ruído. A consequência prática é que a aplicação corre em desenvolvimento, onde o `next dev` "
        "não analisa o código, mas não pode atualmente ser compilada para produção. Corrigi-lo exige "
        "uma entrada de exclusão para o diretório gerado e uma passagem pelos dezasseis erros do "
        "código da aplicação; é uma tarefa curta que não foi feita e é o primeiro item da secção 13.3. "
        "O apêndice C reproduz essa saída na íntegra."
    )

    r.h(2, "10.3 Testes manuais")
    r.p("Os seguintes percursos foram exercitados manual e repetidamente durante o desenvolvimento:")
    r.bullets([
        "acesso não autenticado a rotas protegidas, confirmando a redireção para o início de sessão;",
        "os fluxos de registo e de início de sessão, incluindo a confirmação de que um utilizador "
        "autenticado que peça as páginas de autenticação é redirecionado para fora delas;",
        "criação de agência de ponta a ponta, com os registos resultantes confirmados no MySQL "
        "Workbench;",
        "validação campo a campo, submetendo valores vazios, malformados e fora de intervalo;",
        "carregamento de logótipo, incluindo dimensões deliberadamente incómodas, que foi como o "
        "problema de transbordo da secção 9.9 foi encontrado;",
        "o editor de meta e a caixa de confirmação de eliminação da agência;",
        "criação de subconta a partir do seletor de conta;",
        "comportamento da barra lateral em torno do ponto de rutura médio;",
        "temas claro e escuro.",
    ])
    r.p(
        "Estes testes foram informais: não foram escritos guiões, não foram registados resultados, e "
        "a proteção contra regressões que oferecem vale apenas o que calhou ser reverificado depois "
        "de cada alteração."
    )

    r.h(2, "10.4 O que não foi testado")
    r.p(
        "Não há testes unitários, de integração, de ponta a ponta nem de API. Não há integração "
        "contínua. Não foi feita qualquer medição de carga, latência ou débito, e não foi feita "
        "qualquer medição com o PageSpeed Insights ou o Lighthouse — o que importa, porque o "
        "desempenho faz parte da motivação declarada do projeto, e as secções 11.4 e 13.5 mantêm essa "
        "distinção explícita."
    )
    r.p(
        "Duas categorias de defeito decorrem diretamente desta ausência. Os cenários com vários "
        "utilizadores nunca foram exercitados: o fluxo de convites foi raciocinado mas não executado "
        "com duas contas reais, e a garantia de isolamento entre inquilinos da secção 5.5 nunca foi "
        "testada de forma adversarial. E os erros de lógica que passam a verificação de tipos passam "
        "sem oposição — o defeito de interpolação da secção 7.6 é exatamente o tipo de falha que um "
        "único teste de integração sobre o fluxo de convites teria apanhado de imediato."
    )

    r.h(2, "10.5 Ameaças à validade")
    r.p(
        "As afirmações do capítulo 11 assentam em observação manual feita pelo próprio autor, numa "
        "máquina, contra uma base de dados, num browser. Devem ser lidas como evidência de que os "
        "percursos implementados funcionam em utilização normal, e não como evidência de que estão "
        "corretos sob concorrência, entrada adversarial ou escala. Onde este relatório diz que uma "
        "funcionalidade está implementada, significa que o percurso foi percorrido e os dados "
        "resultantes inspecionados — não que tenha sido verificada."
    )
    r.page_break()

    # ======================================================== 11 RESULTADOS
    r.h(1, "11. Resultados")

    r.h(2, "11.1 O que foi entregue")
    r.p(
        "O Blume funciona. Um visitante consegue chegar ao site de divulgação, criar conta, ser "
        "conduzido ao registo, criar uma agência com formulário validado e logótipo carregado, entrar "
        "na área autenticada por trás de uma verificação de papel, ajustar a meta da agência, criar "
        "uma subconta de cliente através de uma modal e eliminar a agência com confirmação. Por trás "
        "disso, os convites são aceites no primeiro início de sessão, os papéis são propagados para o "
        "fornecedor de identidade, a atividade é registada, a navegação do inquilino é semeada e os "
        "pedidos de subdomínio são reescritos para uma rota dinâmica."
    )
    r.p(
        "O que não foi entregue é igualmente claro: nenhum CRM, nenhum editor de funis, nenhuns sites "
        "publicados, nenhuma biblioteca de multimédia, nenhumas automações, nenhuma faturação e "
        "nenhuma área de subconta."
    )

    r.h(2, "11.2 Objetivos")
    r.table(
        ["Objetivo", "Resultado", "Evidência"],
        [
            ["O1 \u2014 Modelo de dados relacional", ("Alcançado", True),
             "23 modelos e 6 enumerações cobrindo inquilinos, CRM, sites, multimédia, automações e faturação"],
            ["O2 \u2014 Autenticação e autorização por papéis", ("Alcançado", True),
             "Proteção no middleware `Clerk`, verificação de papel no layout da agência, verificação de posse em `deleteAgency`"],
            ["O3 \u2014 Registo da agência", ("Alcançado", True),
             "Formulário validado, carregamento de logótipo, marca branca, editor de meta, eliminação"],
            ["O4 \u2014 Mecanismo de convites", ("Parcialmente alcançado", True),
             "Aceitação implementada e estruturalmente correta; sem interface para emitir convites e com um defeito no nome criado"],
            ["O5 \u2014 Encaminhamento multi-inquilino", ("Parcialmente alcançado", True),
             "Reescrita implementada no middleware; as rotas de destino são esboços e o inquilino não é validado"],
            ["O6 \u2014 Estrutura base da aplicação", ("Parcialmente alcançado", True),
             "Barra lateral, seletor de conta e sistema de modais funcionam; as opções de navegação são semeadas mas não renderizadas"],
            ["O7 \u2014 Experiência prática e documentação honesta", ("Alcançado", True),
             "Um diário de desenvolvimento com 39 entradas numeradas, 73 commits e a análise dos capítulos 8 e 9"],
        ],
        "Avaliação dos objetivos enunciados na secção 1.4.",
        widths=[4.6, 3.0, 9.0], font_size=8.5,
    )
    r.p(
        "Quatro dos sete objetivos foram alcançados e três parcialmente. O padrão nos três parciais é "
        "consistente: em todos, o mecanismo do lado do servidor está completo e falta a superfície "
        "visível ao utilizador. É uma posição mais favorável do que a inversa, mas não é uma "
        "funcionalidade entregue."
    )

    r.h(2, "11.3 O código")
    r.table(
        ["Medida", "Valor"],
        [
            ["Código da aplicação, excluindo primitivas de UI e ícones", "37 ficheiros, 2 533 linhas de TypeScript e TSX"],
            ["Componentes `shadcn/ui` copiados para o projeto", "46 ficheiros"],
            ["Componentes de ícone SVG", "31 ficheiros"],
            ["Total de código do projeto, excluindo código gerado", "114 ficheiros, 8 490 linhas"],
            ["Esquema `Prisma`", "438 linhas; 23 modelos, 6 enumerações"],
            ["Server actions", "10 exportadas, 1 auxiliar privado (nunca chamado)"],
            ["Rotas da aplicação", "8 componentes de página e 1 route handler"],
            ["Dependências", "55 de execução, 9 de desenvolvimento"],
            ["Commits", "73, de 19 de junho de 2025 a 10 de agosto de 2026"],
            ["Testes automatizados", "0"],
        ],
        "Dimensão medida do projeto. O código gerado pelo `Prisma` está excluído em toda a tabela.",
        widths=[7.6, 8.4], font_size=8.5,
    )
    r.p(
        "As contagens de linhas devem ser lidas com cuidado. Cerca de 2 500 linhas são lógica "
        "aplicacional; o restante é código de componentes que o `shadcn/ui` copia para o projeto por "
        "desenho. O projeto caracteriza-se melhor não pelo volume mas pela superfície de integração: "
        "quatro serviços externos, um modelo relacional de 23 entidades e uma camada de encaminhamento "
        "que tem de servir tráfego público, autenticado e por inquilino a partir de uma só instalação."
    )

    r.h(2, "11.4 Estado atual")
    r.p(
        "O resumo honesto é que o Blume é uma fundação funcional e não um produto funcional. As partes "
        "difíceis da plataforma — o modelo de dados multi-inquilino, a autenticação, a camada de "
        "autorização, a infraestrutura de encaminhamento e o percurso de registo — existem e "
        "funcionam. As áreas funcionais que a tornariam útil a uma agência não. A aplicação corre em "
        "desenvolvimento mas não pode atualmente ser compilada para produção."
    )
    r.p(
        "Sobre a questão que motivou o projeto, nada foi demonstrado. Não foi mostrado que o Blume "
        "produza sites com melhores características de desempenho do que o Wix, e não o poderia ter "
        "sido, porque não produz sites. Esse objetivo permanece uma intenção de desenho, e a secção "
        "13.5 enuncia o que seria necessário para o testar."
    )
    r.page_break()

    # ======================================================== 12 DISCUSSÃO
    r.h(1, "12. Discussão")

    r.h(2, "12.1 Pontos fortes")
    r.p(
        "O aspeto mais forte do resultado é a coerência da fundação. A cadeia de propriedade é "
        "consistente, os índices estão completos, papéis e permissões estão modelados a dois níveis "
        "adequados de granularidade, e a camada de encaminhamento trata de forma sensata três tipos "
        "distintos de tráfego. A segurança de tipos flui de ponta a ponta: uma alteração ao esquema "
        "regenera tipos que se propagam para formulários e server actions, pelo que os erros "
        "estruturais surgem em tempo de compilação e não no browser."
    )
    r.p(
        "A concentração de todo o acesso a dados num único módulo de server actions é também um ponto "
        "forte real a esta escala. Todas as consultas do sistema podem ser lidas de uma assentada, o "
        "que foi o que permitiu afirmar com segurança, no capítulo 3, que funcionalidades estão "
        "ligadas e quais não estão."
    )
    r.p(
        "Por fim, o código é invulgarmente honesto sobre o seu próprio estado. O trabalho incompleto "
        "está assinalado com comentários `TODO`, `FIXME` e `WIP` que explicam o que falta e porquê, e "
        "as decisões não óbvias têm comentários que explicam o raciocínio em vez de repetir o código. "
        "Essa convenção veio de uma diretriz escrita adotada a meio do projeto, e é a razão pela qual "
        "este relatório pôde ser reconstruído com rigor a partir do repositório."
    )

    r.h(2, "12.2 Fraquezas e dívida técnica")
    r.p(
        "A fraqueza mais consequente é a ausência de testes automatizados. Tudo o resto nesta secção "
        "é um defeito concreto; este é a razão pela qual tais defeitos sobrevivem. Um código sem "
        "suite de testes não pode ser refactorizado com confiança, e quanto mais cresce mais caro se "
        "torna acrescentá-la."
    )
    r.p(
        "O build de produção que falha é a segunda. É fácil de corrigir e é o tipo de problema que só "
        "se torna visível quando alguém tenta implantar, o que é precisamente a razão por que passou "
        "despercebido."
    )
    r.p("A restante dívida é mais banal:")
    r.bullets([
        "código morto — o auxiliar `getUser` nunca chamado, a variável `allNotifications` não usada, "
        "os ficheiros de tipo de letra Geist órfãos depois da mudança para `DM Sans`;",
        "resíduo da integração `Stripe` removida no handler de submissão do formulário;",
        "o defeito de interpolação em `verifyAndAcceptInvitation` descrito na secção 7.6;",
        "nomes de recursos herdados do tutorial, incluindo um `plura-logo.svg` ainda usado como "
        "logótipo de recurso da barra lateral e na navegação do site;",
        "ausência de histórico de migrações, discutida na secção 6.6;",
        "ausência de dados de exemplo, pelo que avaliar a aplicação exige criar registos à mão;",
        "um padrão de imagem remota em `next.config.mjs` cujo host é a string literal "
        "\u201csubdomain\u201d, com um comentário próprio a assinalar que precisa de correção.",
    ])
    r.p(
        "Nenhum destes pontos é grave isoladamente. No conjunto, são a assinatura de um projeto "
        "desenvolvido primeiro pelas funcionalidades e com a limpeza adiada, que é uma descrição "
        "exata do que aconteceu."
    )

    r.h(2, "12.3 Segurança")
    r.p(
        "Delegar a autenticação no `Clerk` retira ao projeto uma classe inteira de risco. O "
        "armazenamento de credenciais, o hashing de palavras-passe, a emissão de sessões e o suporte "
        "a múltiplos fatores são tratados por um serviço especializado e não por uma implementação de "
        "estudante, e essa é a melhor decisão de segurança do desenho."
    )
    r.p("São conhecidas quatro fraquezas, que devem ser declaradas:")
    r.bullets([
        "**Estado de papel duplicado.** O papel existe no registo `User` e em `privateMetadata` do "
        "`Clerk`, e o layout da agência impõe o acesso usando o segundo. Os metadados privados só são "
        "escritos no servidor, pelo que isto não é diretamente explorável, mas nada mantém as duas "
        "cópias consistentes. Um papel alterado apenas na base de dados não teria efeito; um papel "
        "alterado apenas no `Clerk` teria efeito sem qualquer registo na base de dados. A base de "
        "dados devia ser a fonte autoritativa.",
        "**Carregamentos não associados a um inquilino.** O middleware do `UploadThing` verifica que "
        "quem chama está autenticado mas não regista quem é nem a que inquilino pertence o "
        "carregamento, e `onUploadComplete` não faz nada. Qualquer utilizador autenticado pode "
        "carregar por qualquer rota, e os ficheiros carregados não têm dono até que uma submissão de "
        "formulário guarde o URL.",
        "**As server actions são endpoints alcançáveis.** Assim que uma página que define uma server "
        "action é servida, essa ação passa a ser invocável. A maioria das ações em `queries.ts` confia "
        "nos seus argumentos; `deleteAgency` é a exceção que reverifica a posse na base de dados. "
        "Todas as ações que alteram estado deviam fazer o mesmo.",
        "**Sem limitação de taxa nem proteção contra abuso.** Nada restringe a frequência com que uma "
        "ação ou uma rota de carregamento podem ser chamadas.",
    ])
    r.p(
        "O isolamento entre inquilinos merece nota à parte. É imposto inteiramente pela construção das "
        "consultas, e todas as consultas atualmente no código o fazem corretamente. Mas a garantia é "
        "uma convenção e não uma restrição: nada na base de dados nem no sistema de tipos impediria "
        "que fosse acrescentada uma consulta sem delimitação e, como `relationMode = \"prisma\"` "
        "também remove as chaves estrangeiras, a base de dados não oferece qualquer rede de segurança. "
        "É uma posição razoável para um projeto nesta fase e genuinamente arriscada em escala."
    )

    r.h(2, "12.4 Manutenibilidade")
    r.p(
        "O projeto está bem organizado para a sua dimensão. Rotas, componentes, lógica de servidor e "
        "utilitários partilhados estão separados por diretório; formulários, componentes globais e "
        "primitivas de interface estão distinguidos; e os grupos de rotas mantêm o site de divulgação "
        "e a área autenticada separados sem poluir a estrutura de URL."
    )
    r.p(
        "Duas decisões estruturais não sobreviverão ao crescimento. Concentrar todas as consultas num "
        "módulo é conveniente com dez funções e impraticável com cem; dividi-lo por área de domínio é "
        "o passo seguinte óbvio. E o componente de barra lateral carrega já uma quantidade "
        "considerável de lógica condicional para servir duas apresentações, que é o tipo de "
        "complexidade mais barata de separar do que de continuar a estender."
    )

    r.h(2, "12.5 Escalabilidade")
    r.p(
        "A camada aplicacional não tem estado e escalaria horizontalmente sem alterações. A restrição "
        "é a base de dados, e duas decisões importam. O modelo multi-inquilino de esquema partilhado "
        "implica que todas as consultas filtram por inquilino, o que é eficiente dados os índices que "
        "o esquema declara, mas os dados dos inquilinos ficam entrelaçados, pelo que não há caminho "
        "simples para isolar mais tarde um cliente grande. E `relationMode = \"prisma\"` transfere a "
        "integridade referencial para o cliente, pelo que as eliminações em cascata são emuladas com "
        "consultas adicionais em vez de executadas pela base de dados — aceitável agora, e um custo "
        "que cresce com o volume de dados."
    )
    r.p(
        "Vale a pena notar uma restrição imediata: o pooling de ligações do `Prisma` pressupõe "
        "processos de longa duração. O cliente é guardado em cache em `globalThis` para sobreviver aos "
        "recarregamentos em desenvolvimento, mas implantar numa plataforma serverless exigiria uma "
        "atenção aos limites de ligações que não foi dada."
    )

    r.h(2, "12.6 Desempenho e a motivação original")
    r.p(
        "O desempenho foi motivação fundadora e continua totalmente por medir. A arquitetura é "
        "coerente com a intenção — os componentes de servidor renderizam no servidor e enviam menos "
        "JavaScript do que uma aplicação equivalente renderizada no cliente, o `next/image` trata da "
        "otimização e a framework divide o código por rota — mas coerência com uma intenção não é "
        "evidência."
    )
    r.p(
        "A comparação que motivou o projeto não pode sequer ser feita no estado atual, porque "
        "compararia um site produzido pelo Wix com um site produzido pelo Blume, e o Blume não produz "
        "nenhum. O que podia ser medido hoje é o desempenho da própria página de divulgação do Blume, "
        "o que seria uma medição real de outra coisa. A distinção é mantida explícita porque "
        "confundi-la é exatamente o tipo de afirmação sem suporte que este relatório procura evitar."
    )

    r.h(2, "12.7 Sobre construir a partir de um tutorial")
    r.p(
        "Partir de um tutorial tornou alcançável um projeto desta dimensão dentro do tempo "
        "disponível. Forneceu um modelo de domínio coerente e uma seleção de tecnologias a que teria "
        "levado semanas chegar de forma independente, e removeu o risco de escolher uma arquitetura "
        "que viesse a revelar-se inviável."
    )
    r.p(
        "Impôs também custos que não eram óbvios à partida. O mais significativo foi o desfasamento de "
        "versões: por o material ter um ano, boa parte do esforço foi para diagnosticar falhas que não "
        "eram do projeto, e esse esforço produziu aprendizagem sem produzir funcionalidades. Um custo "
        "mais subtil foi o âmbito herdado. O esquema descreve um produto muito maior do que um único "
        "estudante consegue entregar, e a distância entre esse esquema e a implementação é a principal "
        "razão pela qual este relatório tem de trabalhar tanto para distinguir o que existe do que "
        "está previsto. Reduzir o modelo ao que era realisticamente alcançável teria produzido um "
        "sistema mais pequeno e mais completo."
    )
    r.p(
        "O mais útil que o tutorial forneceu não foi código mas uma sequência — uma ordem defensável "
        "pela qual construir um sistema deste tipo. O mais útil de ele estar desatualizado é que "
        "segui-lo se tornou impossível e compreendê-lo se tornou necessário."
    )

    r.h(2, "12.8 Sobre trabalhar com assistência de IA")
    r.p(
        "Os assistentes usados neste projeto foram mais valiosos quando aplicados a problemas bem "
        "especificados com resultados verificáveis, e menos valiosos quando lhes foi dada margem. Os "
        "modos de falha foram consistentes: alterações que corrigiam um sintoma sem tratar a causa, "
        "alterações que removiam código que estava deliberadamente presente, e alterações que "
        "introduziam ferramentas incoerentes com o projeto — um ficheiro de bloqueio do `npm` num "
        "projeto `Bun` é o exemplo mais claro."
    )
    r.p(
        "A prática que fez diferença foi insistir em compreender uma correção antes de a manter. O "
        "problema de criação de agências da secção 9.7 é o caso mais claro: havia uma correção "
        "funcional disponível, e a decisão de reverter para a versão avariada e reproduzir o problema, "
        "para identificar qual das três causas candidatas era a responsável, produziu conhecimento que "
        "aceitar a correção não teria produzido. A secção 9.5, em que a má leitura de um registo do "
        "servidor conduziu a horas de depuração desnecessária, é o contraexemplo — nenhuma ferramenta "
        "substitui compreender onde o código corre."
    )
    r.page_break()

    # ======================================================== 13 LIMITAÇÕES
    r.h(1, "13. Limitações e Trabalho Futuro")

    r.h(2, "13.1 Limitações funcionais")
    r.bullets([
        "A funcionalidade de construção de sites que motivou o projeto não está implementada. Não "
        "existe editor de páginas, renderizador nem mecanismo de publicação.",
        "Não existe área de subconta. Os utilizadores de subconta são redirecionados para "
        "`/subaccount`, que não resolve para nada; o diretório existe e está vazio.",
        "A navegação da barra lateral não é renderizada, pelo que a área autenticada não pode ser "
        "navegada para além do seletor de conta.",
        "O painel da agência apresenta apenas o identificador da agência.",
        "Os convites podem ser aceites mas não emitidos: não há ecrã de gestão de equipa nem envio de "
        "correio eletrónico.",
        "As notificações são registadas e consultadas mas nunca apresentadas.",
        "Os subsistemas de CRM, multimédia e automações existem apenas como modelos de dados.",
        "A faturação não está implementada sob qualquer forma.",
    ])

    r.h(2, "13.2 Limitações técnicas e dívida")
    r.bullets([
        "O build de produção falha na fase de lint; a aplicação só pode ser executada em "
        "desenvolvimento.",
        "Não existe qualquer cobertura de testes automatizados.",
        "Não existe histórico de migrações; o esquema é aplicado com `db push`.",
        "`relationMode = \"prisma\"` remove chaves estrangeiras de uma base de dados que as suporta, "
        "sem benefício correspondente nesta instalação.",
        "A framework está duas versões maiores atrasada, consequência da decisão de versão descrita na "
        "secção 9.1.",
        "O encaminhamento por subdomínio não valida o inquilino pedido contra a base de dados.",
        "O defeito de interpolação em `verifyAndAcceptInvitation` não está corrigido.",
        "Código morto, recursos órfãos e nomes herdados do tutorial persistem em todo o projeto.",
    ])

    r.h(2, "13.3 Trabalho de curto prazo")
    r.p("O que se segue exigiria pouco tempo e removeria risco desproporcionado:")
    r.bullets([
        "excluir `src/generated` da análise estática e resolver os dezasseis erros do código da "
        "aplicação, para que o build de produção passe;",
        "corrigir o defeito de template literal em `verifyAndAcceptInvitation`;",
        "adotar `prisma migrate dev` e gerar uma migração inicial a partir do esquema atual;",
        "remover `relationMode = \"prisma\"` e deixar o `MySQL` impor a integridade referencial;",
        "acrescentar um script de dados de exemplo, para que a aplicação possa ser avaliada sem "
        "introdução manual de dados;",
        "acrescentar um `.env.example` a documentar a configuração necessária e remover as variáveis "
        "de serviços que não estão integrados;",
        "tornar a base de dados autoritativa quanto aos papéis, lendo do registo `User` em vez dos "
        "metadados do `Clerk`;",
        "associar os carregamentos ao utilizador autenticado e ao seu inquilino no middleware do "
        "`UploadThing`.",
    ])

    r.h(2, "13.4 Trabalho de médio prazo")
    r.p("Pela ordem que o estado atual sugere:")
    r.bullets([
        "renderizar a navegação já semeada na barra lateral, o que desbloqueia todas as áreas "
        "funcionais seguintes;",
        "construir a área de subconta, para que as redireções existentes resolvam;",
        "construir um painel de agência real usando as notificações já registadas;",
        "acrescentar um ecrã de gestão de equipa para que os convites possam ser emitidos, a par do "
        "envio de correio eletrónico;",
        "implementar o subsistema de CRM, cujo modelo já inclui as colunas de ordenação de que uma "
        "interface Kanban precisa;",
        "implementar o editor e o renderizador de funis, persistindo páginas compostas em "
        "`FunnelPage.content` e servindo-as pela reescrita de subdomínio já existente;",
        "introduzir testes automatizados, começando por testes de integração sobre as server actions, "
        "onde o retorno do esforço é maior;",
        "estabelecer um processo de implantação com integração contínua a correr verificação de "
        "tipos, análise estática e testes.",
    ])

    r.h(2, "13.5 Avaliar a questão original de desempenho")
    r.p(
        "A questão que motivou este projeto — se uma plataforma deste tipo consegue gerar sites com "
        "melhor fundação técnica do que um construtor alojado — continua em aberto, e respondê-la é o "
        "trabalho futuro mais interessante disponível."
    )
    r.p("Uma avaliação credível exigiria, no mínimo:")
    r.bullets([
        "um renderizador de funis funcional, para que o Blume produza sequer um site;",
        "o mesmo conteúdo e desenho implementados no Blume e num construtor alojado, para que a "
        "comparação isole a plataforma;",
        "medição repetida com uma ferramenta estabelecida como o PageSpeed Insights ou o Lighthouse, "
        "reportando as Core Web Vitals ao longo de várias execuções e não uma pontuação isolada;",
        "medição em condições comparáveis de rede e de alojamento, já que uma diferença de alojamento "
        "seria de outro modo lida como diferença no código gerado;",
        "reconhecimento explícito do que a comparação não consegue mostrar, dado que um construtor "
        "alojado traz funcionalidade que um renderizador mínimo não tem.",
    ])
    r.p(
        "Enquanto tal avaliação não for feita, o argumento de desempenho a favor do Blume é uma "
        "hipótese. O projeto estabeleceu a arquitetura dentro da qual poderia ser testada, e não a "
        "testou."
    )
    r.page_break()

    # ======================================================== 14 CONCLUSÃO
    r.h(1, "14. Conclusão")
    r.p(
        "Este projeto propôs-se construir uma plataforma multi-inquilino através da qual uma agência "
        "digital pudesse gerir a sua equipa e os espaços de trabalho dos seus clientes. A motivação "
        "foi em parte prática e em parte pessoal: era necessário escolher um projeto final, e um "
        "conceito de construtor de sites encontrado durante a procura de ideias ligou-se a uma "
        "experiência anterior de construção de um site de cliente no Wix, onde o controlo da "
        "plataforma sobre o código gerado tornava impossível trabalhar o desempenho."
    )
    r.p(
        "O sistema entregue é uma aplicação `Next.js` em `TypeScript`, suportada por `MySQL` através "
        "do `Prisma`, com a autenticação delegada no `Clerk` e o armazenamento de ficheiros no "
        "`UploadThing`. Implementa um site de divulgação, autenticação com proteção ao nível da rota, "
        "autorização por papéis, registo de agências com entrada de dados validada e carregamento de "
        "imagem, adesão à equipa por convite, registo de atividade, criação de subcontas e a "
        "infraestrutura de encaminhamento para alojamento por subdomínio. Um esquema de 23 entidades "
        "descreve um produto consideravelmente maior, e este relatório teve o cuidado, do princípio ao "
        "fim, de distinguir essa intenção do que foi efetivamente construído."
    )
    r.p(
        "Os problemas técnicos que moldaram o trabalho foram sobretudo problemas de integração e não "
        "de algoritmo. Um ciclo de redireções que se manifestou como resposta HTTP 431 revelou-se um "
        "matcher de rotas que não contemplava os caminhos aninhados que um fluxo de autenticação gera. "
        "Um diagrama entidade-relação que parecia avariado revelou-se uma representação exata de uma "
        "base de dados à qual uma única definição do ORM tinha removido todas as chaves estrangeiras. "
        "Um formulário que falhava silenciosamente ao guardar revelou-se protegido por uma verificação "
        "sobre um valor que uma integração removida teria fornecido. Em todos os casos o trabalho útil "
        "foi o diagnóstico: formular uma hipótese, ler documentação escrita para a versão atual de uma "
        "biblioteca e não para a do tutorial, e confirmar uma causa antes de aceitar uma correção."
    )
    r.p(
        "O projeto começou por seguir um tutorial, e este relatório disse-o com clareza. A arquitetura "
        "e o modelo de domínio vieram dessa fonte. O que dela não veio foi um sistema funcional: o "
        "tutorial era suficientemente antigo para que boa parte do trabalho fosse traduzir instruções "
        "para bibliotecas que tinham mudado por baixo delas, e quanto mais o projeto avançava menos "
        "podia ser seguido e mais tinha de ser compreendido. A divergência registada na Tabela 6 é a "
        "medida dessa deslocação."
    )
    r.p(
        "O que foi alcançado é uma fundação coerente com uma superfície incompleta. O modelo de dados "
        "multi-inquilino, as camadas de autenticação e autorização, a infraestrutura de encaminhamento "
        "e o percurso de registo funcionam. As áreas funcionais que tornariam a plataforma útil a uma "
        "agência não existem, o build de produção falha atualmente e não há testes automatizados. A "
        "questão de desempenho que motivou o projeto não foi respondida, e não o poderia ter sido, "
        "porque a funcionalidade de geração de sites a que diz respeito nunca chegou a ser atingida."
    )
    r.p(
        "Os resultados mais valiosos não são as funcionalidades. São uma compreensão funcional de onde "
        "o código corre numa framework React moderna e de por que razão isso determina como pode ser "
        "depurado; do que um ORM garante e do que apenas parece garantir; da rapidez com que uma "
        "árvore de dependências envelhece e do que custa recuperar; e da diferença entre uma correção "
        "que remove um sintoma e um diagnóstico que o explica. São essas as partes deste projeto com "
        "maior probabilidade de transitar para o próximo."
    )
    r.page_break()

    # ======================================================== REFERÊNCIAS
    r.h(1, "Referências")
    refs = [
        "Bun. Bun Documentation. https://bun.sh/docs (consultado em agosto de 2026).",
        "Clerk. Clerk Documentation for Next.js. https://clerk.com/docs (consultado em agosto de 2026).",
        "Conventional Commits. Conventional Commits 1.0.0 Specification. "
        "https://www.conventionalcommits.org/en/v1.0.0/ (consultado em agosto de 2026).",
        "Google. Lighthouse. https://developer.chrome.com/docs/lighthouse (consultado em agosto de 2026).",
        "Google. PageSpeed Insights. https://pagespeed.web.dev/ (consultado em agosto de 2026).",
        "Google. Web Vitals. https://web.dev/articles/vitals (consultado em agosto de 2026).",
        "Mozilla. HTTP response status code 431 Request Header Fields Too Large. MDN Web Docs. "
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/431 (consultado em agosto de 2026).",
        "Oracle. MySQL 8.0 Reference Manual. https://dev.mysql.com/doc/refman/8.0/en/ (consultado em agosto de 2026).",
        "Prisma. Prisma ORM Documentation. https://www.prisma.io/docs/orm (consultado em agosto de 2026).",
        "Prisma. Relation mode. https://www.prisma.io/docs/orm/prisma-schema/data-model/relations/relation-mode "
        "(consultado em agosto de 2026).",
        "Radix UI. Radix Primitives Documentation. https://www.radix-ui.com/primitives (consultado em agosto de 2026).",
        "React. React Documentation \u2014 Server Components. https://react.dev/reference/rsc/server-components "
        "(consultado em agosto de 2026).",
        "react-hook-form. Documentation. https://react-hook-form.com/docs (consultado em agosto de 2026).",
        "shadcn. shadcn/ui Documentation. https://ui.shadcn.com/docs (consultado em agosto de 2026).",
        "Tailwind Labs. Tailwind CSS Documentation. https://tailwindcss.com/docs (consultado em agosto de 2026).",
        "TypeScript. TypeScript Handbook. https://www.typescriptlang.org/docs/handbook/intro.html "
        "(consultado em agosto de 2026).",
        "UploadThing. UploadThing Documentation. https://docs.uploadthing.com (consultado em agosto de 2026).",
        "Vercel. Next.js Documentation \u2014 App Router. https://nextjs.org/docs/app (consultado em agosto de 2026).",
        "WebProdigies. Plura \u2014 full-stack agency platform tutorial. YouTube. "
        "https://www.youtube.com/watch?v=6omuUOZcWL0 (consultado em 2025).",
        "Zod. Zod Documentation. https://zod.dev (consultado em agosto de 2026).",
    ]
    for ref in refs:
        p = r.p(ref)
        p.paragraph_format.space_after = Pt(6)
    r.page_break()

    # ======================================================== APÊNDICES
    r.h(1, "Apêndice A \u2014 Entidades de domínio e estado de implementação")
    r.p(
        "Todos os modelos de `prisma/schema.prisma`, com a avaliação de até onde cada um foi levado. "
        "\u201cConsultado\u201d significa que o modelo aparece em pelo menos uma consulta em "
        "`src/lib/queries.ts`. \u201cApenas no esquema\u201d significa que o modelo existe no esquema "
        "e na base de dados e não é referenciado em nenhum ponto do código."
    )
    r.table(
        ["Modelo", "Propósito", "Estado"],
        [
            ["`User`", "Utilizador da aplicação, espelho de uma conta `Clerk`", ("Consultado", True)],
            ["`Agency`", "Inquilino de topo", ("Consultado", True)],
            ["`SubAccount`", "Espaço de trabalho de cliente dentro de uma agência", ("Consultado", True)],
            ["`Permissions`", "Concessão de acesso a uma subconta", ("Consultado", True)],
            ["`Invitation`", "Convite de adesão pendente", ("Consultado", True)],
            ["`Notification`", "Entrada de registo de atividade", ("Consultado, não apresentado", True)],
            ["`AgencySidebarOption`", "Entrada de navegação da agência", ("Criado, não renderizado", True)],
            ["`SubAccountSidebarOption`", "Entrada de navegação da subconta", ("Criado, não renderizado", True)],
            ["`Pipeline`", "Pipeline de CRM pertencente a uma subconta", ("Apenas no esquema", True)],
            ["`Lane`", "Coluna ordenada dentro de um pipeline", ("Apenas no esquema", True)],
            ["`Ticket`", "Cartão dentro de uma lane, com valor e responsável opcionais", ("Apenas no esquema", True)],
            ["`Tag`", "Etiqueta com cor aplicável a tickets", ("Apenas no esquema", True)],
            ["`Contact`", "Contacto de cliente pertencente a uma subconta", ("Apenas no esquema", True)],
            ["`Funnel`", "Um site com subdomínio único opcional", ("Apenas no esquema", True)],
            ["`FunnelPage`", "Página de um funil; conteúdo guardado como `LongText`", ("Apenas no esquema", True)],
            ["`ClassName`", "Estilo nomeado associado a um funil", ("Apenas no esquema", True)],
            ["`Media`", "Recurso carregado pertencente a uma subconta", ("Apenas no esquema", True)],
            ["`Trigger`", "Evento que inicia uma automação", ("Apenas no esquema", True)],
            ["`Automation`", "Sequência de ações ligada a um gatilho", ("Apenas no esquema", True)],
            ["`AutomationInstance`", "Registo de ativação de uma automação", ("Apenas no esquema", True)],
            ["`Action`", "Passo ordenado dentro de uma automação", ("Apenas no esquema", True)],
            ["`Subscription`", "Subscrição de faturação de uma agência", ("Apenas no esquema", True)],
            ["`AddOns`", "Extra adquirível", ("Apenas no esquema", True)],
        ],
        "Os 23 modelos `Prisma` e o respetivo estado na implementação atual.",
        widths=[4.6, 8.0, 4.0], font_size=8.5,
    )
    r.p(
        "As seis enumerações são `Role`, `Icon`, `TriggerTypes`, `ActionType`, `InvitationStatus` e "
        "`Plan`. `Role` e `Icon` são usadas por código da aplicação, e `InvitationStatus` é lida "
        "quando se procura um convite pendente; `TriggerTypes`, `ActionType` e `Plan` não são usadas. "
        "`Plan` é notável por os seus dois membros serem identificadores literais de preço do "
        "`Stripe` herdados do tutorial, o que é uma opção de modelação invulgar e que amarra o esquema "
        "aos identificadores de um sistema externo."
    )
    r.page_break()

    r.h(1, "Apêndice B \u2014 Estrutura do repositório")
    r.p("Organização de diretórios do projeto, excluindo `node_modules`, saída de compilação e código "
        "gerado do cliente.")
    r.code([
        "blume/",
        "\u251c\u2500 prisma/",
        "\u2502  \u2514\u2500 schema.prisma              23 modelos, 6 enums; sem diretorio de migracoes",
        "\u251c\u2500 public/assets/                imagens herdadas do tutorial",
        "\u251c\u2500 src/",
        "\u2502  \u251c\u2500 app/",
        "\u2502  \u2502  \u251c\u2500 site/                   grupo de rotas publicas",
        "\u2502  \u2502  \u251c\u2500 (main)/",
        "\u2502  \u2502  \u2502  \u251c\u2500 agency/",
        "\u2502  \u2502  \u2502  \u2502  \u251c\u2500 (auth)/           rotas catch-all de sign-in e sign-up",
        "\u2502  \u2502  \u2502  \u2502  \u251c\u2500 [agencyId]/       layout do painel com guarda de papel",
        "\u2502  \u2502  \u2502  \u2502  \u251c\u2500 unauthorized/",
        "\u2502  \u2502  \u2502  \u2502  \u2514\u2500 page.tsx          registo e redirecao por papel",
        "\u2502  \u2502  \u2502  \u2514\u2500 subaccount/           diretorio vazio \u2014 destino de redirecao inexistente",
        "\u2502  \u2502  \u251c\u2500 [domain]/               rotas de inquilino por subdominio (esbocos)",
        "\u2502  \u2502  \u2514\u2500 api/uploadthing/        o unico route handler HTTP",
        "\u2502  \u251c\u2500 components/",
        "\u2502  \u2502  \u251c\u2500 forms/                  agency-details, subaccount-details",
        "\u2502  \u2502  \u251c\u2500 global/                 file-upload, custom-modal, loading, mode-toggle",
        "\u2502  \u2502  \u251c\u2500 sidebar/                carregador de servidor e menu de cliente",
        "\u2502  \u2502  \u251c\u2500 site/navigation/",
        "\u2502  \u2502  \u251c\u2500 icons/                  31 componentes de icone SVG",
        "\u2502  \u2502  \u2514\u2500 ui/                     46 componentes shadcn/ui",
        "\u2502  \u251c\u2500 lib/",
        "\u2502  \u2502  \u251c\u2500 db.ts                   singleton do cliente Prisma em globalThis",
        "\u2502  \u2502  \u251c\u2500 queries.ts              10 server actions \u2014 todo o acesso a dados",
        "\u2502  \u2502  \u251c\u2500 constants.ts            cartoes de preco e registo de icones",
        "\u2502  \u2502  \u251c\u2500 uploadthing.ts          auxiliares de cliente tipados",
        "\u2502  \u2502  \u2514\u2500 uploadthing-limits.ts   limite de tamanho partilhado",
        "\u2502  \u251c\u2500 providers/                 provider de tema, provider de modais",
        "\u2502  \u2514\u2500 middleware.ts              autenticacao, redirecoes, reescrita de subdominio",
        "\u251c\u2500 diagrams/                     esboco Excalidraw, modelo Workbench",
        "\u2514\u2500 package.json                  55 dependencias de execucao e 9 de desenvolvimento",
    ])
    r.page_break()

    r.h(1, "Apêndice C \u2014 Saída da análise estática")
    r.p(
        "Saída de `bun run lint`, restrita ao código da aplicação. Os erros reportados em "
        "`src/generated/prisma` estão omitidos; são código gerado por máquina e representam a grande "
        "maioria do total. Esta é a saída referida na secção 10.2."
    )
    r.code([
        "./src/app/(main)/agency/[agencyId]/layout.tsx",
        "34:27  Error: Unexpected any. Specify a different type.",
        "37:7   Error: 'allNotifications' is assigned a value but never used.",
        "",
        "./src/app/(main)/agency/unauthorized/page.tsx",
        "4:14   Error: The `{}` (\"empty object\") type allows any non-nullish value.",
        "6:15   Error: 'props' is defined but never used.",
        "",
        "./src/components/forms/agency-details.tsx",
        "100:6  Warning: React Hook useEffect has a missing dependency: 'form'.",
        "105:11 Error: 'custId' is defined but never used.",
        "107:15 Error: 'bodyData' is assigned a value but never used.",
        "129:7  Error: 'newUserData' is assigned a value but never used.",
        "129:7  Error: 'newUserData' is never reassigned. Use 'const' instead.",
        "",
        "./src/components/forms/subaccount-details.tsx",
        "60:3   Error: 'userId' is defined but never used.",
        "88:6   Warning: React Hook useEffect has a missing dependency: 'form'.",
        "",
        "./src/components/sidebar/menu-options.tsx",
        "26:12  Error: Unexpected any. Specify a different type.",
        "27:9   Error: Unexpected any. Specify a different type.",
        "31:50  Error: 'sidebarOptions' is defined but never used.",
        "31:94  Error: 'id' is defined but never used.",
        "",
        "./src/components/site/navigation/index.tsx",
        "16:23  Error: 'user' is defined but never used.",
        "",
        "./src/components/unauthorized/index.tsx",
        "4:14   Error: The `{}` (\"empty object\") type allows any non-nullish value.",
        "6:23   Error: 'props' is defined but never used.",
    ])
    r.p(
        "Vários destes são mais do que problemas de estilo. A propriedade `sidebarOptions` não usada é "
        "a navegação não renderizada da secção 6.3; a variável `allNotifications` não usada é a "
        "funcionalidade de notificações não apresentada da secção 7.7; `custId` e `bodyData` são o "
        "resíduo da integração `Stripe` removida, descrita na secção 9.7."
    )
