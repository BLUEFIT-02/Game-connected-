from pathlib import Path
from math import atan2, cos, sin, pi

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "14-diagrammi-completi.pdf"
PAGE_W, PAGE_H = landscape(A4)

PURPLE = colors.HexColor("#8b6cf0")
BOX_FILL = colors.HexColor("#ededff")
GROUP_FILL = colors.HexColor("#ffffdf")
GROUP_STROKE = colors.HexColor("#b8b83f")
BLACK = colors.HexColor("#222222")
GRAY = colors.HexColor("#777777")


def fit(text, font="Helvetica", max_size=12, width=100):
    size = max_size
    while size > 5 and stringWidth(text, font, size) > width:
        size -= 0.5
    return size


def lines(text, width, font="Helvetica", size=10):
    out, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def box(c, x, y, w, h, text, size=11, bold=False, fill=BOX_FILL, stroke=PURPLE):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=1)
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFillColor(colors.black)
    c.setFont(font, fit(text, font, size, w - 0.35 * cm))
    ll = lines(text, w - 0.35 * cm, font, size)
    total = len(ll) * size * 1.25
    yy = y + h / 2 + total / 2 - size
    for line in ll:
        c.drawCentredString(x + w / 2, yy, line)
        yy -= size * 1.25


def group(c, x, y, w, h, title):
    c.setFillColor(GROUP_FILL)
    c.setStrokeColor(GROUP_STROKE)
    c.setLineWidth(0.8)
    c.rect(x, y, w, h, fill=1, stroke=1)
    c.setFillColor(BLACK)
    c.setFont("Helvetica", 13)
    c.drawCentredString(x + w / 2, y + h - 0.35 * cm, title)


def arrow(c, x1, y1, x2, y2, label="", dashed=False, color=BLACK):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(0.8)
    if dashed:
        c.setDash(3, 3)
    c.line(x1, y1, x2, y2)
    c.setDash()
    ang = atan2(y2 - y1, x2 - x1)
    size = 6
    pts = [
        (x2, y2),
        (x2 - size * cos(ang - pi / 7), y2 - size * sin(ang - pi / 7)),
        (x2 - size * cos(ang + pi / 7), y2 - size * sin(ang + pi / 7)),
    ]
    p = c.beginPath()
    p.moveTo(*pts[0])
    p.lineTo(*pts[1])
    p.lineTo(*pts[2])
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    if label:
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 9)
        c.drawCentredString((x1 + x2) / 2, (y1 + y2) / 2 + 0.13 * cm, label)


def class_box(c, x, y, w, h, title, body):
    c.setFillColor(BOX_FILL)
    c.setStrokeColor(PURPLE)
    c.setLineWidth(0.8)
    c.rect(x, y, w, h, fill=1, stroke=1)
    c.line(x, y + h - 0.45 * cm, x + w, y + h - 0.45 * cm)
    c.line(x, y + h - 0.95 * cm, x + w, y + h - 0.95 * cm)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 7.3)
    c.drawCentredString(x + w / 2, y + h - 0.30 * cm, title)
    c.setFont("Helvetica", 6.5)
    c.drawString(x + 0.12 * cm, y + 0.30 * cm, body)


def lifelines(c, names, top=15.0 * cm, bottom=1.8 * cm):
    margin = 1.65 * cm
    step = (PAGE_W - 2 * margin) / (len(names) - 1)
    xs = []
    for i, name in enumerate(names):
        x = margin + i * step
        xs.append(x)
        box(c, x - 1.25 * cm, top, 2.5 * cm, 0.85 * cm, name, 10)
        box(c, x - 1.25 * cm, bottom - 0.6 * cm, 2.5 * cm, 0.85 * cm, name, 10)
        c.setStrokeColor(PURPLE)
        c.setLineWidth(1.0)
        c.line(x, top, x, bottom)
    return xs


def msg(c, xs, src, dst, y, label, dashed=False):
    arrow(c, xs[src], y, xs[dst], y, label, dashed=dashed)


def page_header(c, title):
    c.setFillColor(BLACK)
    c.setFont("Helvetica", 14)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 0.65 * cm, title)


def page_1_architecture(c):
    group(c, 0.2 * cm, 11.8 * cm, 16.4 * cm, 3.8 * cm, "Edge")
    box(c, 0.9 * cm, 13.25 * cm, 4.1 * cm, 0.9 * cm, "Interfaccia locale")
    box(c, 6.6 * cm, 13.25 * cm, 4.3 * cm, 0.9 * cm, "Express API locale")
    box(c, 12.6 * cm, 14.1 * cm, 3.1 * cm, 0.9 * cm, "Coda JSON")
    box(c, 12.5 * cm, 12.4 * cm, 3.3 * cm, 0.9 * cm, "Client MQTT")
    arrow(c, 5.0 * cm, 13.7 * cm, 6.6 * cm, 13.7 * cm)
    arrow(c, 10.9 * cm, 13.85 * cm, 12.6 * cm, 14.55 * cm)
    arrow(c, 10.9 * cm, 13.4 * cm, 12.5 * cm, 12.85 * cm)

    group(c, 17.3 * cm, 9.6 * cm, 9.1 * cm, 6.9 * cm, "Frontend")
    box(c, 18.5 * cm, 13.25 * cm, 3.4 * cm, 0.9 * cm, "Pagine HTML")
    box(c, 18.0 * cm, 10.6 * cm, 4.4 * cm, 0.9 * cm, "JavaScript browser")
    box(c, 23.4 * cm, 10.6 * cm, 1.9 * cm, 0.9 * cm, "CSS")
    arrow(c, 20.2 * cm, 13.25 * cm, 20.2 * cm, 11.5 * cm)

    group(c, 16.8 * cm, 6.8 * cm, 6.9 * cm, 2.1 * cm, "Gateway")
    box(c, 17.55 * cm, 7.25 * cm, 5.4 * cm, 1.1 * cm, "server.js - instradamento")
    group(c, 16.9 * cm, 0.25 * cm, 8.0 * cm, 5.45 * cm, "Backend")
    backend_y = [4.55, 3.55, 2.55, 1.55]
    for i, name in enumerate(["Routes", "Middleware", "Controllers", "Services"]):
        box(c, 19.0 * cm, backend_y[i] * cm, 2.4 * cm, 0.72 * cm, name)
        if i:
            arrow(c, 20.2 * cm, backend_y[i - 1] * cm, 20.2 * cm, (backend_y[i] + 0.72) * cm)
    box(c, 17.75 * cm, 0.55 * cm, 3.0 * cm, 0.72 * cm, "Utils/Rules")
    box(c, 22.1 * cm, 0.55 * cm, 2.1 * cm, 0.72 * cm, "db.js")
    arrow(c, 20.2 * cm, 6.8 * cm, 20.2 * cm, 5.7 * cm)


def page_2_use_cases(c):
    actors = [
        ("Admin piattaforma", ["Gestire locali", "Gestire utenti", "Creare tornei", "Scegliere locali e squadre", "Vedere statistiche globali"], 0.5, 3.1),
        ("Admin gioco", ["Definire tipi di gioco", "Definire regole eventi", "Definire modelli sensore"], 7.7, 6.1),
        ("Admin locale", ["Gestire giochi del locale", "Gestire edge e sensori", "Gestire attuatori", "Creare squadre", "Avviare partite", "Vedere statistiche locali"], 14.3, 4.6),
        ("Giocatore", ["Vedere giochi", "Vedere proprie partite", "Vedere statistiche", "Vedere tornei"], 21.0, 5.5),
    ]
    for actor, cases, xcm, ycm in actors:
        x, y = xcm * cm, ycm * cm
        box(c, x, y, 2.3 * cm, 0.75 * cm, actor, 8)
        for i, uc in enumerate(cases):
            yy = y + (len(cases) - 1) * 0.55 * cm / 2 - i * 0.9 * cm
            xx = x + 3.5 * cm
            box(c, xx, yy, 3.2 * cm, 0.65 * cm, uc, 6.8)
            arrow(c, x + 2.3 * cm, y + 0.37 * cm, xx, yy + 0.32 * cm)


def page_3_domain(c):
    items = {
        "Tournament": (10.3, 14.2, 4.5, 1.25, "id name game_type participant_mode status"),
        "Locale": (1.7, 10.8, 2.3, 1.25, ""),
        "GameType": (13.0, 11.0, 4.7, 1.25, "id name description score_limit supports_teams"),
        "User": (23.4, 9.2, 3.5, 1.25, "id username password role locale_id"),
        "EdgeDevice": (0.2, 7.2, 3.8, 1.25, "id name status last_seen last_sync"),
        "Game": (4.4, 7.2, 4.1, 1.25, "id name type status locale_id game_type_id"),
        "SensorTemplate": (18.7, 7.2, 3.6, 1.25, "id name event_type description"),
        "Team": (16.5, 6.7, 2.4, 1.25, "id name locale_id"),
        "Sensor": (0.1, 4.6, 3.8, 1.25, "id name sensor_type mqtt_topic status"),
        "Actuator": (4.35, 4.6, 3.9, 1.25, "id name actuator_type state mqtt_topic"),
        "Match": (8.8, 4.6, 6.4, 1.25, "id participant_mode player1_name player2_name score1 score2 status"),
        "TeamMember": (20.3, 4.8, 1.5, 0.9, ""),
        "MatchEvent": (9.55, 2.1, 4.8, 1.25, "id event_uuid event_type sync_status created_at"),
    }
    center = {}
    for name, (x, y, w, h, body) in items.items():
        class_box(c, x * cm, y * cm, w * cm, h * cm, name, body)
        center[name] = ((x + w / 2) * cm, (y + h / 2) * cm)
    rels = [("Tournament","Locale"),("Tournament","GameType"),("Tournament","Team"),("Locale","EdgeDevice"),("Locale","Game"),("Locale","Team"),("GameType","Game"),("GameType","SensorTemplate"),("EdgeDevice","Sensor"),("Game","Sensor"),("Game","Actuator"),("Game","Match"),("Match","MatchEvent"),("User","TeamMember"),("Team","TeamMember"),("Tournament","Match")]
    for a, b in rels:
        arrow(c, *center[a], *center[b], color=GRAY)


def page_4_modules(c):
    modules = [
        ("ApiGateway", "serviceFor(path) forwardRequest() health()", 7.2, 14.7, 3.9),
        ("UserController", "getUsers() createClient() createLocalAdmin() createGameAdmin()", 11.6, 14.7, 5.7),
        ("DeviceController", "getDevices() createSensor() createActuator()", 17.7, 14.7, 4.3),
        ("EdgeService", "publishOrQueue() syncQueue() simulate()", 22.4, 14.7, 4.4),
        ("GameTypeController", "getGameTypes() createGameType() createSensorTemplate()", 4.65, 12.8, 5.5),
        ("MatchController", "startMatch() addMatchEvent() simulateMatchMqtt()", 12.6, 12.8, 4.7),
        ("AuthController", "login()", 17.8, 12.8, 1.45),
        ("TournamentController", "createTournament() addMatchToTournament()", 0.55, 10.4, 4.5),
        ("ValidationRules", "validateGameTypeInput() validateTournamentInput() validateMatchParticipants()", 5.5, 10.4, 6.8),
        ("MatchEventService", "processMatchEvent() getMatchRow() getMatchEvents()", 12.85, 10.4, 5.1),
        ("TournamentService", "getTournamentMatches() getTournamentRankingRows()", 0.35, 7.8, 5.15),
        ("ActuatorService", "updateActuators()", 14.35, 7.8, 2.25),
        ("TournamentRules", "calculateTournamentRanking() isTournamentMatchCompatible()", 0.05, 5.4, 5.7),
    ]
    centers = {}
    for title, body, x, y, w in modules:
        class_box(c, x * cm, y * cm, w * cm, 1.05 * cm, title, body)
        centers[title] = ((x + w / 2) * cm, (y + 0.52) * cm)
    for a, b in [("ApiGateway","TournamentController"),("GameTypeController","ValidationRules"),("MatchController","ValidationRules"),("MatchController","MatchEventService"),("UserController","AuthController"),("DeviceController","AuthController"),("MatchEventService","TournamentService"),("MatchEventService","ActuatorService"),("TournamentController","TournamentService"),("TournamentService","TournamentRules")]:
        arrow(c, *centers[a], *centers[b], color=GRAY)


def page_5_micro(c):
    box(c, 0.1 * cm, 8.0 * cm, 1.8 * cm, 0.8 * cm, "Browser")
    box(c, 4.7 * cm, 8.0 * cm, 1.9 * cm, 0.8 * cm, "Gateway")
    box(c, 11.5 * cm, 10.3 * cm, 2.6 * cm, 0.8 * cm, "Match Service")
    box(c, 11.4 * cm, 7.4 * cm, 2.7 * cm, 0.8 * cm, "Catalog Service")
    box(c, 11.2 * cm, 3.8 * cm, 3.2 * cm, 0.8 * cm, "Tournament Service")
    box(c, 19.0 * cm, 4.3 * cm, 1.2 * cm, 1.0 * cm, "MySQL")
    box(c, 18.8 * cm, 14.3 * cm, 2.0 * cm, 0.8 * cm, "Mosquitto")
    box(c, 24.8 * cm, 7.3 * cm, 1.5 * cm, 0.8 * cm, "Edge")
    notes = [("Match logic: punteggio,\nUUID, eventi", 3.75, 11.2), ("Catalog logic: ruoli,\nconfigurazione,\ninventario", 3.75, 5.5), ("Tournament logic:\ncalendario,\ncompatibilita, classifica", 3.75, 1.8), ("Edge logic: sensori,\ncoda offline, heartbeat", 18.2, 4.9)]
    for txt, x, y in notes:
        box(c, x * cm, y * cm, 3.8 * cm, 1.25 * cm, txt.replace("\n", " "))
    arrow(c, 1.9 * cm, 8.4 * cm, 4.7 * cm, 8.4 * cm, "REST /api")
    arrow(c, 6.6 * cm, 8.4 * cm, 11.5 * cm, 10.7 * cm, "matches")
    arrow(c, 6.6 * cm, 8.1 * cm, 11.4 * cm, 7.8 * cm, "auth users locales games")
    arrow(c, 6.6 * cm, 7.9 * cm, 11.2 * cm, 4.2 * cm, "teams tournaments statistics")
    for target in [(19.0, 4.8), (19.0, 4.8), (19.0, 4.8)]:
        pass
    arrow(c, 14.1 * cm, 10.7 * cm, 19.0 * cm, 4.8 * cm)
    arrow(c, 14.1 * cm, 7.8 * cm, 19.0 * cm, 4.8 * cm)
    arrow(c, 14.4 * cm, 4.2 * cm, 19.0 * cm, 4.8 * cm)
    arrow(c, 25.5 * cm, 8.1 * cm, 20.8 * cm, 14.7 * cm, "MQTT eventi sensori")
    arrow(c, 18.8 * cm, 14.7 * cm, 14.1 * cm, 10.7 * cm, "MQTT comandi attuatori")


def page_6_login(c):
    xs = lifelines(c, ["Utente", "Browser", "API Gateway", "Catalog Service", "MySQL"])
    y = 14.0 * cm
    for src, dst, lab, dashed in [(0,1,"username e password",False),(1,2,"POST /api/auth/login",False),(2,3,"inoltra richiesta",False),(3,4,"SELECT user",False),(4,3,"utente e ruolo",True),(3,2,"JSON utente",True),(2,1,"risposta",True),(1,0,"dashboard del ruolo",True)]:
        msg(c, xs, src, dst, y, lab, dashed)
        y -= 1.0 * cm


def page_7_match(c):
    xs = lifelines(c, ["Admin locale", "Frontend", "Gateway", "Match Service", "Edge Service", "MQTT Broker", "MySQL"])
    y = 14.6 * cm
    for src, dst, lab, dashed in [(0,1,"Avvia partita",False),(1,2,"POST /api/matches/start",False),(2,3,"richiesta",False),(3,6,"INSERT match + UPDATE game",False),(3,1,"match LIVE",True),(0,1,"Simula MQTT",False),(1,2,"POST /matches/id/simulate-mqtt",False),(2,3,"richiesta",False),(3,4,"POST /simulate",False),(4,5,"publish evento QoS 1",False),(5,3,"evento MQTT",False),(3,6,"controllo UUID e UPDATE punteggio",False),(3,5,"comando attuatore",False),(5,4,"stato display/LED",False)]:
        msg(c, xs, src, dst, y, lab, dashed)
        y -= 0.75 * cm


def page_8_offline(c):
    xs = lifelines(c, ["Sensore simulato", "Edge", "Broker", "Match Service", "MySQL"])
    y = 14.4 * cm
    msg(c, xs, 0, 1, y, "evento")
    y -= 0.8 * cm
    c.setStrokeColor(PURPLE)
    c.setDash(2, 2)
    c.rect(xs[1] - 2.8 * cm, y - 3.0 * cm, xs[2] - xs[1] + 3.1 * cm, 3.25 * cm, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(BLACK)
    c.setFont("Helvetica", 10)
    c.drawString(xs[1] + 1.8 * cm, y, "[MQTT offline]")
    c.drawString(xs[1] - 2.6 * cm, y - 1.1 * cm, "salva evento PENDING in JSON")
    y -= 3.4 * cm
    c.drawString(xs[1] + 1.8 * cm, y + 0.3 * cm, "[MQTT online]")
    msg(c, xs, 1, 2, y, "publish evento")
    y -= 1.0 * cm
    msg(c, xs, 1, 2, y, "riconnessione")
    y -= 1.0 * cm
    c.drawString(xs[1] - 1.0 * cm, y + 0.2 * cm, "legge coda")
    y -= 1.0 * cm
    msg(c, xs, 1, 2, y, "ripubblica evento con stesso UUID")
    y -= 1.0 * cm
    msg(c, xs, 2, 3, y, "evento")
    y -= 0.8 * cm
    msg(c, xs, 3, 4, y, "verifica UUID")
    y -= 0.6 * cm
    msg(c, xs, 3, 4, y, "salva una sola volta")


def page_9_tournament(c):
    xs = lifelines(c, ["Admin piattaforma", "Frontend", "Tournament Service", "MySQL"])
    y = 14.2 * cm
    for src, dst, lab, dashed in [(0,1,"crea torneo con locali e modalita",False),(1,2,"POST /api/tournaments",False),(2,3,"INSERT tournament",False),(2,3,"INSERT tournament_locations",False),(2,3,"INSERT tournament_teams",False),(0,1,"collega partita e turno",False),(1,2,"POST /tournaments/id/matches",False),(2,3,"verifica tipo, modalita, locale e stato",False),(2,3,"INSERT tournament_matches",False),(2,3,"SELECT partite concluse",False),(2,1,"classifica calcolata",True)]:
        msg(c, xs, src, dst, y, lab, dashed)
        y -= 0.85 * cm


def page_10_deployment(c):
    box(c, 7.7 * cm, 14.2 * cm, 4.9 * cm, 0.9 * cm, "Computer studente")
    nodes = {
        "frontend :8080": (2.6, 11.8, 4.1, 0.9),
        "api-gateway :3000": (7.75, 11.8, 4.8, 0.9),
        "edge-service :8090": (21.3, 8.7, 4.9, 0.9),
        "catalog-service :3001\ninterno": (0.2, 7.6, 5.9, 1.15),
        "match-service :3002\ninterno": (7.2, 7.6, 5.9, 1.15),
        "tournament-service\n:3003 interno": (14.25, 7.6, 5.9, 1.15),
        "mysql :3306": (8.4, 3.9, 2.6, 1.0),
        "mosquitto :1883": (20.8, 3.8, 4.2, 0.9),
    }
    centers = {}
    for name, (x, y, w, h) in nodes.items():
        box(c, x * cm, y * cm, w * cm, h * cm, name.replace("\n", " "), 10)
        centers[name] = ((x + w / 2) * cm, (y + h / 2) * cm)
    for n in ["frontend :8080", "api-gateway :3000", "edge-service :8090"]:
        arrow(c, 10.1 * cm, 14.2 * cm, *centers[n])
    for n in ["catalog-service :3001\ninterno", "match-service :3002\ninterno", "tournament-service\n:3003 interno"]:
        arrow(c, *centers["api-gateway :3000"], *centers[n])
        arrow(c, *centers[n], *centers["mysql :3306"])
    arrow(c, *centers["edge-service :8090"], *centers["mosquitto :1883"])
    arrow(c, *centers["match-service :3002\ninterno"], *centers["mosquitto :1883"])


def page_11_summary(c):
    page_header(c, "Legenda per la discussione orale")
    rows = [
        ("REST", "browser e gateway usano richieste/risposte per gestire dati"),
        ("MQTT", "edge e match service scambiano eventi e comandi tramite broker"),
        ("Edge", "simula sensori, conserva coda JSON offline, sincronizza al ritorno online"),
        ("UUID", "impedisce di contare due volte lo stesso evento con QoS 1"),
        ("Microservizi", "catalogo, partite e tornei hanno responsabilita separate"),
        ("Limite didattico", "database condiviso e autenticazione semplificata dopo login"),
    ]
    y = 13.5 * cm
    for k, v in rows:
        box(c, 4.0 * cm, y, 4.0 * cm, 0.8 * cm, k, 10)
        box(c, 9.0 * cm, y, 12.5 * cm, 0.8 * cm, v, 9)
        y -= 1.25 * cm


PAGES = [
    ("Architettura package", page_1_architecture),
    ("Casi d'uso", page_2_use_cases),
    ("Dominio dati", page_3_domain),
    ("Moduli implementativi", page_4_modules),
    ("Microservizi e flussi", page_5_micro),
    ("Sequenza login", page_6_login),
    ("Sequenza partita MQTT", page_7_match),
    ("Sequenza offline", page_8_offline),
    ("Sequenza torneo", page_9_tournament),
    ("Deployment Docker", page_10_deployment),
    ("Sintesi orale", page_11_summary),
]


def main():
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4))
    for title, fn in PAGES:
        page_header(c, title)
        fn(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
