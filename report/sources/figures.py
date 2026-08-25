"""Gera as figuras do relatório a partir de factos verificados no repositório.

Os rótulos descritivos estão em português; os identificadores de código,
ficheiros e tecnologias mantêm a grafia original em inglês, tal como aparecem
no código-fonte.
"""
import os
os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.path.dirname(__file__), ".mplcache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

INK = "#1a1a1a"
GREY = "#5c5c5c"
LIGHT = "#f4f4f6"
MID = "#e2e4e8"
ACCENT = "#d7e3f7"
WARN = "#fbecd2"
PLAN = "#ebebee"


def box(ax, x, y, w, h, text, fc=LIGHT, ec=INK, lw=0.9, fs=8.5, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.004,rounding_size=0.015",
                                facecolor=fc, edgecolor=ec, linewidth=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=INK, weight=weight, linespacing=1.5)


def arrow(ax, p1, p2, ls="-", color=INK, lw=0.9, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", linestyle=ls, color=color,
                                 linewidth=lw, mutation_scale=10,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=1.0, shrinkB=1.0))


def route(ax, pts, ls="-", color=INK, lw=0.9):
    """Ligação ortogonal por vários troços, para contornar caixas."""
    xs = [p[0] for p in pts[:-1]]
    ys = [p[1] for p in pts[:-1]]
    ax.plot(xs, ys, ls=ls, color=color, lw=lw, solid_capstyle="butt")
    arrow(ax, pts[-2], pts[-1], ls=ls, color=color, lw=lw)


def note(ax, x, y, text, fs=7.4, ha="left", color=GREY, style="normal"):
    ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va="center",
            linespacing=1.5, style=style)


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=220, bbox_inches="tight",
                pad_inches=0.08, facecolor="white")
    plt.close(fig)
    print("escrita", name)


# ============================================================ Figura 1
fig, ax = canvas(8.2, 5.4)

box(ax, 0.045, 0.880, 0.30, 0.090, "Navegador\ncomponentes cliente React", fc=MID, weight="bold", fs=8.5)

ax.add_patch(Rectangle((0.012, 0.085), 0.628, 0.700, facecolor="white",
                       edgecolor=GREY, linewidth=0.9, linestyle=(0, (4, 3))))
note(ax, 0.335, 0.752, "Aplicação Next.js 14  —  App Router",
     fs=8.2, ha="center", style="italic")

box(ax, 0.060, 0.615, 0.555, 0.098,
    "src/middleware.ts\nverificação de sessão  \u00b7  proteção de rotas\nredireção da raiz  \u00b7  reescrita de subdomínio",
    fc=ACCENT, fs=7.8)
box(ax, 0.060, 0.425, 0.255, 0.145,
    "React Server\nComponents\n/site  \u00b7  /agency\n/agency/[agencyId]\n/[domain]", fs=6.8)
box(ax, 0.360, 0.425, 0.255, 0.145,
    "Server Actions\nsrc/lib/queries.ts\n(\"use server\")\n10 funções exportadas", fs=7.1)
box(ax, 0.360, 0.255, 0.255, 0.098, "Prisma Client 6.9\ngerado em\nsrc/generated/prisma", fs=7.8)
box(ax, 0.360, 0.105, 0.255, 0.098, "Route Handler\n/api/uploadthing\n(único endpoint HTTP)", fs=7.4)

box(ax, 0.700, 0.880, 0.29, 0.090, "Clerk\nidentidade como serviço", fc=WARN, fs=8.5)
box(ax, 0.700, 0.252, 0.29, 0.104, "MySQL\n23 tabelas\nsem chaves estrangeiras", fc=WARN, fs=8.0)
box(ax, 0.700, 0.102, 0.29, 0.104, "UploadThing v7\narmazenamento\nde ficheiros", fc=WARN, fs=8.0)

arrow(ax, (0.190, 0.880), (0.190, 0.713))
note(ax, 0.205, 0.800, "HTTPS", fs=7.4)
arrow(ax, (0.345, 0.925), (0.700, 0.925))
note(ax, 0.522, 0.950, "interface de sign-in / sign-up", fs=7.4, ha="center")

arrow(ax, (0.187, 0.615), (0.187, 0.570))
arrow(ax, (0.487, 0.615), (0.487, 0.570))
arrow(ax, (0.315, 0.497), (0.360, 0.497))
arrow(ax, (0.487, 0.425), (0.487, 0.353))
route(ax, [(0.060, 0.664), (0.032, 0.664), (0.032, 0.154), (0.360, 0.154)])

arrow(ax, (0.615, 0.304), (0.700, 0.304))
note(ax, 0.670, 0.332, "SQL", fs=7.4, ha="center")
arrow(ax, (0.615, 0.154), (0.700, 0.154), ls=(0, (3, 2)))
arrow(ax, (0.618, 0.705), (0.721, 0.876), color=GREY, rad=0.16)
note(ax, 0.715, 0.790, "verificação\nde sessão", fs=7.2)

note(ax, 0.012, 0.038,
     "Setas cheias: fluxo de pedidos e de dados.  Seta tracejada: envio de ficheiros por URL pré-assinado.\n"
     "A aplicação não expõe API REST ou GraphQL pública; todo o acesso a dados ocorre no servidor, através do Prisma.")
save(fig, "fig1_architecture.png")


# ============================================================ Figura 2
fig, ax = canvas(7.4, 6.6)

L, W = 0.03, 0.545       # coluna das decisões
RX, RW = 0.635, 0.345    # coluna dos resultados
H = 0.092

steps = [
    (0.900, "Pedido recebido", MID, "bold", None),
    (0.782, "rota == \"/\"", ACCENT, "normal", "redireciona \u2192 /site"),
    (0.664, "sessão iniciada  e  rota é\n/agency/sign-in ou /agency/sign-up", ACCENT, "normal", "redireciona \u2192 /agency"),
    (0.546, "rota == \"/sign-in\"  ou  \"/sign-up\"", ACCENT, "normal", "redireciona \u2192 /agency/sign-in"),
    (0.428, "rota pública?\n/site, /agency/sign-in(.*),\n/agency/sign-up(.*), /api/uploadthing", ACCENT, "normal", "não \u2192 await auth.protect()"),
    (0.310, "host é subdomínio de\nNEXT_PUBLIC_DOMAIN", ACCENT, "normal", "reescreve \u2192 /<inquilino><rota>"),
    (0.192, "rota começa por\n/agency  ou  /subaccount", ACCENT, "normal", "reescreve \u2192 mesma rota"),
    (0.074, "NextResponse.next()", MID, "bold", None),
]

for y, label, fc, weight, out in steps:
    h = H
    box(ax, L, y, W, h, label, fc=fc, weight=weight, fs=7.9)
    if out:
        box(ax, RX, y, RW, h, out, fc=LIGHT, fs=7.9)
        arrow(ax, (L + W, y + h / 2), (RX, y + h / 2))
        ax.text((L + W + RX) / 2, y + h / 2 + 0.019, "sim" if not out.startswith("não") else "",
                ha="center", va="bottom", fontsize=7, color=GREY)

for i in range(len(steps) - 1):
    y_from = steps[i][0]
    y_to = steps[i + 1][0]
    h_to = H
    arrow(ax, (L + W / 2, y_from), (L + W / 2, y_to + h_to))
    if i > 0:
        ax.text(L + W / 2 + 0.016, (y_from + y_to + h_to) / 2, "não",
                ha="left", va="center", fontsize=7, color=GREY)

note(ax, 0.03, 0.022,
     "Fonte: src/middleware.ts. A proteção de rotas corre depois das regras de redireção e antes das reescritas\n"
     "multi-inquilino, pelo que pedidos não autenticados nunca chegam à fase de reescrita.")
save(fig, "fig2_middleware.png")


# ============================================================ Figura 3
fig, ax = canvas(8.4, 5.6)

lanes = ["Utilizador", "Middleware", "/agency\ncomponente de servidor",
         "queries.ts\nserver actions", "MySQL  /  Clerk"]
xs = [0.085, 0.285, 0.495, 0.715, 0.925]
for x, name in zip(xs, lanes):
    ax.text(x, 0.955, name, ha="center", va="center", fontsize=8, weight="bold",
            color=INK, linespacing=1.4)
    ax.plot([x, x], [0.085, 0.905], color=MID, linewidth=1.1, zorder=0)


def msg(y, i, j, label, ls="-", fs=7.4):
    arrow(ax, (xs[i], y), (xs[j], y), ls=ls)
    ax.text((xs[i] + xs[j]) / 2, y + 0.016, label, ha="center", va="bottom",
            fontsize=fs, color=INK, linespacing=1.4,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.6))


msg(0.868, 0, 1, "GET /agency")
msg(0.806, 1, 4, "verifica a sessão Clerk")
msg(0.744, 1, 2, "autorizado \u2192 renderiza")
msg(0.682, 2, 3, "verifyAndAcceptInvitation()")
msg(0.620, 3, 4, "procura Invitation PENDING pelo e-mail")
msg(0.530, 3, 4, "createTeamUser, apaga o convite,\ndefine privateMetadata.role no Clerk", ls=(0, (3, 2)))
msg(0.470, 2, 3, "getAuthUserDetails()")
msg(0.408, 3, 4, "User + Agency + SubAccount + Permissions")

box(ax, 0.145, 0.246, 0.725, 0.146,
    "com agencyId  \u2192  redireção conforme o papel:\n"
    "SUBACCOUNT_USER | SUBACCOUNT_GUEST \u2192 /subaccount\n"
    "AGENCY_OWNER | AGENCY_ADMIN \u2192 /agency/<id>\n"
    "sem agencyId  \u2192  renderiza o formulário de registo <AgencyDetails/>", fc=ACCENT, fs=7.4)

msg(0.186, 0, 3, "submete o formulário \u2192 initUser() e depois upsertAgency()")
msg(0.130, 3, 4, "upsert de User e de Agency,\ncria 6 registos AgencySidebarOption")
arrow(ax, (xs[3], 0.084), (xs[0], 0.084))
ax.text((xs[0] + xs[3]) / 2, 0.100, "router.refresh() \u2192 /agency/<id>", ha="center", va="bottom",
        fontsize=7.4, color=INK, bbox=dict(facecolor="white", edgecolor="none", pad=0.6))

note(ax, 0.02, 0.033,
     "Seta tracejada: executada apenas quando existe um convite pendente para o e-mail com sessão iniciada.\n"
     "Fontes: src/app/(main)/agency/page.tsx, src/lib/queries.ts, src/components/forms/agency-details.tsx", fs=7.1)
save(fig, "fig3_onboarding_flow.png")


# ============================================================ Figura 4
fig, ax = canvas(8.4, 6.5)


def entity(x, y_top, w, title, fields, fc=ACCENT):
    head = 0.052
    h = head + 0.036 * len(fields) + 0.016
    ax.add_patch(FancyBboxPatch((x, y_top - h), w, h,
                                boxstyle="round,pad=0.003,rounding_size=0.010",
                                facecolor="white", edgecolor=INK, linewidth=0.9))
    ax.add_patch(Rectangle((x, y_top - head), w, head, facecolor=fc,
                           edgecolor=INK, linewidth=0.9))
    ax.text(x + w / 2, y_top - head / 2, title, ha="center", va="center",
            fontsize=8.2, weight="bold")
    for k, f in enumerate(fields):
        ax.text(x + 0.013, y_top - head - 0.026 - 0.036 * k, f,
                ha="left", va="center", fontsize=7.0)
    return dict(x=x, y=y_top, w=w, h=h, bot=y_top - h, cx=x + w / 2)


AG = entity(0.335, 0.982, 0.315, "Agency",
            ["id  PK (uuid)", "name, agencyLogo, companyEmail", "address, city, state, zipCode, country",
             "whiteLabel : Boolean", "goal : Int (por omissão 5)"])
US = entity(0.020, 0.690, 0.275, "User",
            ["id  PK", "email  ÚNICO", "name, avatarUrl", "role : Role", "agencyId \u2192 Agency"])
SA = entity(0.690, 0.690, 0.290, "SubAccount",
            ["id  PK", "name, subAccountLogo", "companyEmail, companyPhone", "address \u2026 , goal",
             "agencyId \u2192 Agency"])
PE = entity(0.020, 0.360, 0.275, "Permissions",
            ["id  PK", "email \u2192 User.email", "subAccountId \u2192 SubAccount", "access : Boolean"])
NO = entity(0.335, 0.360, 0.315, "Notification",
            ["id  PK", "notification : String", "userId \u2192 User, agencyId \u2192 Agency",
             "subAccountId \u2192 SubAccount (anulável)"])
IN = entity(0.690, 0.360, 0.290, "Invitation",
            ["id  PK", "email  ÚNICO", "agencyId \u2192 Agency", "status : InvitationStatus",
             "role : Role"])


def card(x, y, t):
    ax.text(x, y, t, fontsize=6.9, color=GREY, ha="center", va="center",
            bbox=dict(facecolor="white", edgecolor="none", pad=0.6))


arrow(ax, (US["cx"], US["y"]), (AG["x"], AG["y"] - AG["h"] + 0.02))
card(0.258, 0.772, "1 : N")
arrow(ax, (SA["cx"], SA["y"]), (AG["x"] + AG["w"], AG["y"] - AG["h"] + 0.02))
card(0.726, 0.772, "1 : N")
arrow(ax, (US["cx"], US["bot"]), (PE["cx"], PE["y"]))
card(US["cx"] + 0.042, 0.415, "1 : N")
arrow(ax, (SA["x"], SA["bot"] + 0.02), (PE["x"] + PE["w"], PE["y"] - 0.030), rad=-0.13, color=GREY)
card(0.500, 0.478, "1 : N")
arrow(ax, (AG["cx"], AG["bot"]), (NO["cx"], NO["y"]), color=GREY)
card(AG["cx"] + 0.036, 0.560, "1 : N")
arrow(ax, (AG["x"] + AG["w"], AG["bot"] + 0.02), (IN["cx"] + 0.06, IN["y"]), rad=-0.30, color=GREY)
card(0.655, 0.585, "1 : N")
arrow(ax, (US["x"] + US["w"], US["bot"] - 0.015), (NO["x"], NO["y"] - 0.050), rad=-0.12, color=GREY)
card(0.316, 0.278, "1 : N")

note(ax, 0.02, 0.050,
     "Apresentam-se apenas as seis entidades usadas pelo código atual; os restantes 17 modelos são agrupados na figura seguinte.\n"
     "As relações estão declaradas em prisma/schema.prisma, mas como está definido relationMode = \"prisma\" o MySQL não guarda\n"
     "restrições de chave estrangeira: cada relação assenta num @@index explícito e é garantida pelo Prisma em tempo de consulta.", fs=7.1)
save(fig, "fig4_er_core.png")


# ============================================================ Figura 5
fig, ax = canvas(8.0, 4.6)

groups = [
    (0.02, 0.615, 0.305, 0.315, "Identidade e inquilinos", ACCENT,
     "User   Agency   SubAccount\nPermissions   Invitation\nNotification", "implementado"),
    (0.345, 0.615, 0.305, 0.315, "Navegação", ACCENT,
     "AgencySidebarOption\nSubAccountSidebarOption", "em desenvolvimento"),
    (0.670, 0.615, 0.305, 0.315, "Faturação", PLAN,
     "Subscription   AddOns\nenum Plan", "planeado"),
    (0.02, 0.245, 0.305, 0.315, "CRM", PLAN,
     "Pipeline   Lane   Ticket\nTag   Contact", "planeado"),
    (0.345, 0.245, 0.305, 0.315, "Sites e multimédia", PLAN,
     "Funnel   FunnelPage\nClassName   Media", "planeado"),
    (0.670, 0.245, 0.305, 0.315, "Automações", PLAN,
     "Trigger   Automation\nAutomationInstance   Action", "planeado"),
]
for x, y, w, h, title, fc, members, status in groups:
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.005,rounding_size=0.018",
                                facecolor=fc, edgecolor=INK, linewidth=0.9))
    ax.text(x + w / 2, y + h - 0.052, title, ha="center", va="center", fontsize=8.6, weight="bold")
    ax.text(x + w / 2, y + h / 2 - 0.020, members, ha="center", va="center",
            fontsize=7.5, linespacing=1.9)
    ax.text(x + w / 2, y + 0.038, status, ha="center", va="center", fontsize=7.0,
            color=GREY, style="italic")

note(ax, 0.02, 0.105,
     "Os 23 modelos e 6 enumerações estão declarados em prisma/schema.prisma e aplicados ao MySQL. Os grupos sombreados estão\n"
     "modelados e aguardam implementação: o esquema descreve o domínio completo desde o início, para que cada área funcional\n"
     "possa ser construída sem reestruturar a base de dados.")
save(fig, "fig5_domain_groups.png")


# ============================================================ Figura 6
fig, ax = plt.subplots(figsize=(6.8, 2.9))
months = ["2025-06", "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
          "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08"]
counts = [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 25, 15, 19, 10]
bars = ax.bar(range(len(months)), counts, color="#5b7fb3", edgecolor=INK, linewidth=0.5, width=0.66)
ax.set_xticks(range(len(months)))
ax.set_xticklabels(months, rotation=55, ha="right", fontsize=7.2)
ax.set_ylabel("commits", fontsize=8.5)
ax.tick_params(axis="y", labelsize=7.5)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color=MID, linewidth=0.6)
ax.set_axisbelow(True)
for b, c in zip(bars, counts):
    if c:
        ax.text(b.get_x() + b.get_width() / 2, c + 0.6, str(c), ha="center", fontsize=7)
ax.set_ylim(0, 29)
fig.savefig(os.path.join(OUT, "fig6_commits.png"), dpi=220, bbox_inches="tight",
            pad_inches=0.08, facecolor="white")
plt.close(fig)
print("escrita fig6_commits.png")
