import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ==========================
# HERENCIAS
# ==========================

personajes = {

    "E": [
        "Usopp", "Koby", "Konohamaru", "Sakura", "Hinata",
        "Armin", "Mumen Rider", "Yamcha", "Krillin", "Chopper",
        "Taiju Oki", "Mineta", "Denji", "Iruma Suzuki",
        "Zenitsu", "Shikamaru", "Ino", "Kiba", "Nami",
        "Tenten", "Choji", "Buggy", "Atsushi Nakajima",
        "Maka Albarn", "Tamaki Kotatsu", "Momo Yaoyorozu",
        "Takemichi Hanagaki"
    ],

    "D": [
        "Tanjiro", "Inosuke", "Nezuko", "Megumi",
        "Nobara", "Yuji", "Asta", "Noelle", "Luck",
        "Mikasa", "Levi", "Killua", "Gon",
        "Kirishima", "Kaminari", "Gray", "Natsu",
        "Gaara", "Todoroki", "Deku",
        "Shinra Kusakabe", "Arthur Boyle",
        "Power", "Edward Elric",
        "Akame", "Tatsumi",
        "Bell Cranel", "Ochaco Uraraka",
        "Yuno", "Magna Swing"
    ],

    "C": [
        "Kakashi", "Zoro", "Sanji", "Law",
        "Crocodile", "Smoker", "Todo Aoi",
        "Yuta Okkotsu", "Erza Scarlet",
        "Gajeel", "Ban", "King",
        "Dabi", "Hawks", "Endeavor",
        "Kisame", "Deidara", "Sasori",
        "Benimaru", "Mereoleona",
        "Rengoku", "Tengen Uzui",
        "Shinobu", "Genos", "Garou",
        "Kurapika", "Hisoka",
        "Tokoyami", "Byakuya", "Renji"
    ],

    "B": [
        "Itachi", "Pain", "Obito",
        "Minato", "Yami",
        "Julius Novachrono",
        "All Might", "Katakuri",
        "Marco", "Sabo",
        "Aokiji", "Akainu", "Kizaru",
        "Escanor", "Kenpachi",
        "Doflamingo", "Rayleigh",
        "Eustass Kid",
        "Hashirama", "Tobirama",
        "Oden", "Toji Fushiguro",
        "Muichiro Tokito",
        "Giyu Tomioka",
        "Yoruichi"
    ],

    "A": [
        "Naruto", "Sasuke", "Luffy", "Ichigo",
        "Madara", "Shanks", "Kaido", "Big Mom",
        "Whitebeard", "Meliodas", "Gojo", "Sukuna"
    ],

    "S": [
        "Arthur Leywin",
        "Satoru Gojo",
        "Ryomen Sukuna"
    ]
}

# ==========================
# PROBABILIDADES
# ==========================

clases = (
    ["E"] * 40 +
    ["D"] * 25 +
    ["C"] * 18 +
    ["B"] * 10 +
    ["A"] * 5 +
    ["S"] * 2
)

# ==========================
# NIVELES DE RECOMPENSA
# ==========================

NIVELES_RECOMPENSA = {3, 6, 9, 12, 15, 20, 25, 30, 40, 50, 75, 100}

# ==========================
# EXPERIENCIA
# ==========================

def exp_necesaria(nivel):
    return nivel * 250

# ==========================
# BASE DE DATOS JSON
# ==========================

def cargar_datos():
    if not os.path.exists("datos.json"):
        return {}
    with open("datos.json", "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(datos):
    with open("datos.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def cargar_objetos():
    if not os.path.exists("objetos.json"):
        return {}
    with open("objetos.json", "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_objetos(objetos):
    with open("objetos.json", "w", encoding="utf-8") as f:
        json.dump(objetos, f, indent=4, ensure_ascii=False)

# ==========================
# POOL DE PERSONAJES
# ==========================

def cargar_pool():
    if not os.path.exists("pool.json"):
        pool = {tier: list(pjs) for tier, pjs in personajes.items()}
        guardar_pool(pool)
        return pool
    with open("pool.json", "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_pool(pool):
    with open("pool.json", "w", encoding="utf-8") as f:
        json.dump(pool, f, indent=4, ensure_ascii=False)

def sacar_personaje(pool, clase):
    tiers_orden = ["E", "D", "C", "B", "A", "S"]
    if pool.get(clase):
        herencia = random.choice(pool[clase])
        pool[clase].remove(herencia)
        return herencia, clase
    for tier in tiers_orden:
        if pool.get(tier):
            herencia = random.choice(pool[tier])
            pool[tier].remove(herencia)
            return herencia, tier
    return None, None

def devolver_personaje(pool, clase, herencia):
    if clase not in pool:
        pool[clase] = []
    if herencia not in pool[clase]:
        pool[clase].append(herencia)

# ==========================
# BOT LISTO
# ==========================

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("-------------------")
    print("EL SISTEMA ONLINE")
    print(bot.user)
    print("-------------------")

# ==========================
# /DESPERTAR
# ==========================

@bot.tree.command(name="despertar", description="Obtén tu herencia.")
async def despertar(interaction: discord.Interaction):

    datos = cargar_datos()
    pool = cargar_pool()
    usuario = str(interaction.user.id)

    if usuario in datos:
        await interaction.response.send_message("⚠️ Ya has realizado tu despertar.", ephemeral=True)
        return

    if sum(len(v) for v in pool.values()) == 0:
        await interaction.response.send_message("❌ No quedan personajes disponibles.", ephemeral=True)
        return

    clase = random.choice(clases)
    herencia, clase_final = sacar_personaje(pool, clase)

    if herencia is None:
        await interaction.response.send_message("❌ No quedan personajes disponibles.", ephemeral=True)
        return

    datos[usuario] = {
        "nombre": interaction.user.name,
        "clase": clase_final,
        "herencia": herencia,
        "nivel": 1,
        "exp": 0,
        "recompensas": [],
        "recompensa_pendiente": None,
        "inventario": {}
    }

    guardar_datos(datos)
    guardar_pool(pool)

    await interaction.response.send_message(
f"""
# 🎰 EL JUEGO HA INICIADO

**Clase:** {clase_final}

**Herencia:**
{herencia}

**Nivel:** 1

**EXP:** 0

Bienvenido al Sistema.
"""
    )

# ==========================
# /MIFICHA
# ==========================

@bot.tree.command(name="mificha", description="Ver tu ficha.")
async def mificha(interaction: discord.Interaction):

    datos = cargar_datos()
    usuario = str(interaction.user.id)

    if usuario not in datos:
        await interaction.response.send_message("⚠️ Primero utiliza /despertar", ephemeral=True)
        return

    pj = datos[usuario]
    recompensas = pj.get("recompensas", [])
    recompensas_txt = "\n".join(f"• {r}" for r in recompensas) if recompensas else "Ninguna"

    pendiente_txt = ""
    if pj.get("recompensa_pendiente"):
        rp = pj["recompensa_pendiente"]
        if rp.get("opciones"):
            pendiente_txt = "\n\n🎁 **¡Tienes una recompensa pendiente!** Usa **/elegir_recompensa**"
        else:
            pendiente_txt = "\n\n🔔 **Recompensa pendiente** — Esperando al administrador."

    await interaction.response.send_message(
f"""
# 📋 FICHA

**Nombre:** {pj['nombre']}

**Clase:** {pj['clase']}

**Herencia:** {pj['herencia']}

**Nivel:** {pj['nivel']}

**EXP:** {pj['exp']}/{exp_necesaria(pj['nivel'])}

**Recompensas obtenidas:**
{recompensas_txt}{pendiente_txt}
"""
    )

# ==========================
# /VER_FICHA
# ==========================

@bot.tree.command(name="ver_ficha", description="Ver la ficha de cualquier jugador.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(usuario="Jugador a consultar")
async def ver_ficha(interaction: discord.Interaction, usuario: discord.Member):

    datos = cargar_datos()
    user_id = str(usuario.id)

    if user_id not in datos:
        await interaction.response.send_message("⚠️ Ese usuario no ha despertado.", ephemeral=True)
        return

    pj = datos[user_id]
    recompensas = pj.get("recompensas", [])
    recompensas_txt = "\n".join(f"• {r}" for r in recompensas) if recompensas else "Ninguna"

    pendiente = pj.get("recompensa_pendiente")
    pendiente_txt = ""
    if pendiente:
        if pendiente.get("opciones"):
            opciones_txt = "\n".join(f"  {i+1}. {op}" for i, op in enumerate(pendiente["opciones"]))
            pendiente_txt = f"\n\n🎁 **Recompensa pendiente (Nv.{pendiente['nivel']}):**\n{opciones_txt}"
        else:
            pendiente_txt = f"\n\n🔔 **Recompensa pendiente** (Nv.{pendiente['nivel']}) — sin opciones aún."

    await interaction.response.send_message(
f"""
# 📋 FICHA — {usuario.mention}

**Nombre:** {pj['nombre']}

**Clase:** {pj['clase']}

**Herencia:** {pj['herencia']}

**Nivel:** {pj['nivel']}

**EXP:** {pj['exp']}/{exp_necesaria(pj['nivel'])}

**Recompensas obtenidas:**
{recompensas_txt}{pendiente_txt}
""",
        ephemeral=True
    )

# ==========================
# /PERSONAJES
# ==========================

@bot.tree.command(name="personajes", description="Ver los personajes disponibles por tier.")
async def personajes_cmd(interaction: discord.Interaction):

    pool = cargar_pool()
    tiers_orden = ["S", "A", "B", "C", "D", "E"]
    lineas = []

    for tier in tiers_orden:
        disponibles = pool.get(tier, [])
        lineas.append(f"**[{tier}]** {len(disponibles)}/{len(personajes[tier])} disponibles")
        if disponibles:
            lineas.append(", ".join(disponibles))
        lineas.append("")

    await interaction.response.send_message(
f"""
# 📜 PERSONAJES DISPONIBLES

{"".join(lineas)}
""",
        ephemeral=True
    )

# ==========================
# /DAR_EXP
# ==========================

@bot.tree.command(name="dar_exp", description="Dar experiencia a un jugador.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(usuario="Usuario que recibirá EXP", cantidad="Cantidad de EXP")
async def dar_exp(interaction: discord.Interaction, usuario: discord.Member, cantidad: int):

    datos = cargar_datos()
    user_id = str(usuario.id)

    if user_id not in datos:
        await interaction.response.send_message("⚠️ Ese usuario no ha despertado.", ephemeral=True)
        return

    datos[user_id]["exp"] += cantidad
    niveles_ganados = 0
    recompensas_desbloqueadas = []

    while datos[user_id]["exp"] >= exp_necesaria(datos[user_id]["nivel"]):
        datos[user_id]["exp"] -= exp_necesaria(datos[user_id]["nivel"])
        datos[user_id]["nivel"] += 1
        niveles_ganados += 1
        if datos[user_id]["nivel"] in NIVELES_RECOMPENSA:
            if not datos[user_id].get("recompensa_pendiente"):
                datos[user_id]["recompensa_pendiente"] = {
                    "nivel": datos[user_id]["nivel"],
                    "opciones": []
                }
                recompensas_desbloqueadas.append(datos[user_id]["nivel"])

    guardar_datos(datos)

    nivel = datos[user_id]["nivel"]
    recompensa_txt = ""
    if recompensas_desbloqueadas:
        recompensa_txt = f"\n\n🔔 **¡RECOMPENSA PENDIENTE! (Nv.{recompensas_desbloqueadas[0]})**\nUsa **/crear_recompensa** para configurar las opciones."

    await interaction.response.send_message(
f"""
✅ {usuario.mention} recibió {cantidad} EXP

📈 Nivel actual: {nivel}

⭐ EXP actual:
{datos[user_id]["exp"]}/{exp_necesaria(nivel)}

⬆️ Niveles ganados:
{niveles_ganados}{recompensa_txt}
"""
    )

# ==========================
# /CREAR_RECOMPENSA
# ==========================

@bot.tree.command(name="crear_recompensa", description="Crear opciones de recompensa para un jugador.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    usuario="Jugador que recibirá la recompensa",
    opcion1="Primera opción",
    opcion2="Segunda opción",
    opcion3="Tercera opción"
)
async def crear_recompensa(
    interaction: discord.Interaction,
    usuario: discord.Member,
    opcion1: str,
    opcion2: str,
    opcion3: str
):

    datos = cargar_datos()
    user_id = str(usuario.id)

    if user_id not in datos:
        await interaction.response.send_message("⚠️ Ese usuario no ha despertado.", ephemeral=True)
        return

    if not datos[user_id].get("recompensa_pendiente"):
        datos[user_id]["recompensa_pendiente"] = {"nivel": datos[user_id]["nivel"], "opciones": []}

    datos[user_id]["recompensa_pendiente"]["opciones"] = [opcion1, opcion2, opcion3]
    guardar_datos(datos)

    nivel = datos[user_id]["recompensa_pendiente"]["nivel"]

    await interaction.response.send_message(
f"""
# 🎁 NUEVA RECOMPENSA — {usuario.mention}

**Nivel desbloqueado:** {nivel}

1️⃣ {opcion1}

2️⃣ {opcion2}

3️⃣ {opcion3}

Usa **/elegir_recompensa** para elegir.
"""
    )

# ==========================
# /ELEGIR_RECOMPENSA
# ==========================

@bot.tree.command(name="elegir_recompensa", description="Elige tu recompensa.")
@app_commands.describe(opcion="Número de opción (1, 2 o 3)")
async def elegir_recompensa(interaction: discord.Interaction, opcion: int):

    datos = cargar_datos()
    usuario = str(interaction.user.id)

    if usuario not in datos:
        await interaction.response.send_message("⚠️ Primero utiliza /despertar", ephemeral=True)
        return

    pendiente = datos[usuario].get("recompensa_pendiente")

    if not pendiente:
        await interaction.response.send_message("⚠️ No tienes ninguna recompensa pendiente.", ephemeral=True)
        return

    opciones = pendiente.get("opciones", [])

    if not opciones:
        await interaction.response.send_message("⏳ Espera a que un administrador configure las opciones.", ephemeral=True)
        return

    if opcion < 1 or opcion > len(opciones):
        await interaction.response.send_message(f"⚠️ Elige una opción entre 1 y {len(opciones)}.", ephemeral=True)
        return

    elegida = opciones[opcion - 1]
    datos[usuario].setdefault("recompensas", []).append(elegida)
    datos[usuario]["recompensa_pendiente"] = None
    guardar_datos(datos)

    await interaction.response.send_message(
f"""
# 🎉 ¡Has obtenido!

**{elegida}**

Ha sido añadido a tu ficha.
"""
    )

# ==========================
# /CREAR_OBJETO
# ==========================

@bot.tree.command(name="crear_objeto", description="Crear un nuevo objeto.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    nombre="Nombre del objeto",
    descripcion="Descripción del objeto",
    rareza="Rareza (Común, Poco Común, Raro, Épico, Legendario, Mítico, Divino)",
    imagen="URL de la imagen (opcional)"
)
async def crear_objeto(
    interaction: discord.Interaction,
    nombre: str,
    descripcion: str,
    rareza: str,
    imagen: str = None
):

    objetos = cargar_objetos()

    if nombre in objetos:
        await interaction.response.send_message(f"⚠️ Ya existe **{nombre}**. Usa **/editar_objeto**.", ephemeral=True)
        return

    objetos[nombre] = {"descripcion": descripcion, "rareza": rareza, "imagen": imagen or ""}
    guardar_objetos(objetos)

    await interaction.response.send_message(f"✅ Objeto **{nombre}** creado. Rareza: {rareza}", ephemeral=True)

# ==========================
# /EDITAR_OBJETO
# ==========================

@bot.tree.command(name="editar_objeto", description="Editar un objeto existente.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    objeto="Nombre del objeto a editar",
    descripcion="Nueva descripción (opcional)",
    rareza="Nueva rareza (opcional)",
    imagen="Nueva URL de imagen (opcional)"
)
async def editar_objeto(
    interaction: discord.Interaction,
    objeto: str,
    descripcion: str = None,
    rareza: str = None,
    imagen: str = None
):

    objetos = cargar_objetos()

    if objeto not in objetos:
        await interaction.response.send_message(f"⚠️ No existe **{objeto}**.", ephemeral=True)
        return

    if descripcion: objetos[objeto]["descripcion"] = descripcion
    if rareza: objetos[objeto]["rareza"] = rareza
    if imagen: objetos[objeto]["imagen"] = imagen

    guardar_objetos(objetos)
    await interaction.response.send_message(f"✅ **{objeto}** actualizado.", ephemeral=True)

# ==========================
# /BORRAR_OBJETO
# ==========================

@bot.tree.command(name="borrar_objeto", description="Eliminar un objeto.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(objeto="Nombre del objeto a eliminar")
async def borrar_objeto(interaction: discord.Interaction, objeto: str):

    objetos = cargar_objetos()

    if objeto not in objetos:
        await interaction.response.send_message(f"⚠️ No existe **{objeto}**.", ephemeral=True)
        return

    del objetos[objeto]
    guardar_objetos(objetos)
    await interaction.response.send_message(f"🗑️ **{objeto}** eliminado.", ephemeral=True)

# ==========================
# /OBJETO
# ==========================

@bot.tree.command(name="objeto", description="Ver la información de un objeto.")
@app_commands.describe(nombre="Nombre del objeto")
async def objeto_cmd(interaction: discord.Interaction, nombre: str):

    objetos = cargar_objetos()

    if nombre not in objetos:
        await interaction.response.send_message(f"⚠️ No existe **{nombre}**.", ephemeral=True)
        return

    obj = objetos[nombre]
    embed = discord.Embed(title=f"📦 {nombre}", description=obj["descripcion"], color=discord.Color.gold())
    embed.add_field(name="Rareza", value=obj["rareza"], inline=True)
    if obj.get("imagen"):
        embed.set_image(url=obj["imagen"])

    await interaction.response.send_message(embed=embed)

# ==========================
# /DAR_OBJETO
# ==========================

@bot.tree.command(name="dar_objeto", description="Dar un objeto a un jugador.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    usuario="Jugador que recibirá el objeto",
    objeto="Nombre del objeto",
    cantidad="Cantidad a dar"
)
async def dar_objeto(
    interaction: discord.Interaction,
    usuario: discord.Member,
    objeto: str,
    cantidad: int
):

    datos = cargar_datos()
    objetos = cargar_objetos()
    user_id = str(usuario.id)

    if user_id not in datos:
        await interaction.response.send_message("⚠️ Ese usuario no ha despertado.", ephemeral=True)
        return

    if objeto not in objetos:
        await interaction.response.send_message(f"⚠️ No existe **{objeto}**. Créalo con **/crear_objeto**.", ephemeral=True)
        return

    datos[user_id].setdefault("inventario", {})[objeto] = datos[user_id]["inventario"].get(objeto, 0) + cantidad
    guardar_datos(datos)

    await interaction.response.send_message(f"🎁 {usuario.mention} recibió **{objeto} x{cantidad}**")

# ==========================
# /INVENTARIO
# ==========================

@bot.tree.command(name="inventario", description="Ver tu inventario.")
async def inventario(interaction: discord.Interaction):

    datos = cargar_datos()
    usuario = str(interaction.user.id)

    if usuario not in datos:
        await interaction.response.send_message("⚠️ Primero utiliza /despertar", ephemeral=True)
        return

    inv = datos[usuario].get("inventario", {})
    contenido = "\n".join(f"**{obj}** x{cant}" for obj, cant in inv.items()) if inv else "Tu inventario está vacío."

    await interaction.response.send_message(
f"""
# 📦 Inventario de {datos[usuario]['nombre']}

{contenido}
"""
    )

# ==========================
# /RANKING
# ==========================

@bot.tree.command(name="ranking", description="Ver el top de jugadores.")
async def ranking(interaction: discord.Interaction):

    datos = cargar_datos()

    if not datos:
        await interaction.response.send_message("⚠️ No hay jugadores registrados aún.", ephemeral=True)
        return

    ordenados = sorted(datos.items(), key=lambda x: (x[1]["nivel"], x[1]["exp"]), reverse=True)
    medals = ["🥇", "🥈", "🥉"]
    lineas = []

    for i, (uid, pj) in enumerate(ordenados[:10]):
        medalla = medals[i] if i < 3 else f"{i + 1}."
        lineas.append(
            f"{medalla} **{pj['nombre']}** — "
            f"Clase {pj['clase']} | "
            f"Nv.{pj['nivel']} | "
            f"{pj['exp']}/{exp_necesaria(pj['nivel'])} EXP"
        )
    tabla = "\n".join(lineas)
    await interaction.response.send_message(
f"""
# 🏆 RANKING
{tabla}
"""
    )
# ==========================
# /RESETEAR
# ==========================
@bot.tree.command(name="resetear", description="Reiniciar el progreso de un jugador.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(usuario="Usuario a resetear")
async def resetear(interaction: discord.Interaction, usuario: discord.Member):
    datos = cargar_datos()
    pool = cargar_pool()
    user_id = str(usuario.id)
    if user_id not in datos:
        await interaction.response.send_message("⚠️ Ese usuario no ha despertado.", ephemeral=True)
        return
    pj = datos[user_id]
    devolver_personaje(pool, pj["clase"], pj["herencia"])
    del datos[user_id]
    guardar_datos(datos)
    guardar_pool(pool)
    await interaction.response.send_message(
f"""
🗑️ El progreso de {usuario.mention} ha sido reiniciado.
**{pj['herencia']}** ha vuelto al pool disponible.
Puede usar **/despertar** para comenzar de nuevo.
"""
    )
# ==========================
# INICIAR BOT
# ==========================
bot.run(TOKEN)
