"""Tests d'acceptation de la curation de la Couche jeu (issue #10).

Seams testés (interfaces publiques observables, pas d'implémentation) :
- l'arbre `skills/game/` : la Couche jeu curatée
- le `router` : entrée unique qui pointe les clés conservées
"""

import re
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
COUCHE_JEU = RACINE / "skills" / "game"
ROUTER = COUCHE_JEU / "router"

# Les 7 clés curatées + game-jam en réserve (issue #10, critères d'acceptation).
SKILLS_GARDES = {
    # 1. router — point d'entrée unique
    "router",
    # 2. prototype-fast
    "prototype-fast",
    # 3. level-design
    "level-design",
    # 4. game-feel (+ camera-systems, godot-animation)
    "game-feel",
    "camera-systems",
    "godot-animation",
    # 5. socle GDScript-first
    "godot-gdscript",
    "godot-nodes-scenes",
    "godot-signals-groups",
    "godot-resources",
    # 6. performance-optimization (+ binôme physics-tuning)
    "performance-optimization",
    "physics-tuning",
    # 7. export + publish
    "godot-export",
    "itch-publish",
    "steam-publish",
    # réserve
    "game-jam",
}

# Les 28 skills retirés de la Couche jeu (issue #10). Source unique de vérité :
# le router ne doit en citer aucun, et aucun skill gardé ne doit y renvoyer.
# « multiplayer », « mono » et « PhantomCamera » n'y figurent pas : ce sont des
# concepts/termes Godot, pas des skills retirés.
SKILLS_ECARTES = [
    # les 9 genres
    "platformer", "roguelike", "rpg", "fps-shooter", "tower-defense",
    "card-game", "visual-novel", "survival-crafting", "puzzle",
    # moteur / réseau / 3D / assets
    "godot-csharp", "godot-multiplayer", "godot-3d-essentials",
    "create-game-assets",
    # disciplines et primitives hors socle
    "game-ai", "ai-behavior-trees-utility-ai", "audio-design",
    "dialogue-systems", "procedural-gen", "save-systems",
    "shader-programming", "input-systems", "game-ui-ux",
    "godot-2d-movement", "godot-tilemap", "godot-physics",
    "godot-ui-control", "godot-shaders", "godot-audio",
]
MOTIFS_SKILLS_ECARTES = [rf"\b{re.escape(s)}\b" for s in SKILLS_ECARTES]

# Termes d'autres moteurs : la Couche jeu est Godot-only (critère « refs non-Godot »).
MOTS_AUTRES_MOTEURS = [
    r"\bunity\b",
    r"\bunreal\b",
    r"\broblox\b",
    r"\bbevy\b",
    r"\bphaser\b",
    r"\bpixijs?\b",
    r"\bpygame\b",
    r"\bcinemachine\b",
    r"\bweb-engines\b",
    r"\bother-engines\b",
]

# API d'autres moteurs qui ont survécu à une purge purement lexicale : les noms
# de types/méthodes sont eux aussi du bruit non-Godot.
API_AUTRES_MOTEURS = [
    r"\bSmoothDamp\b",
    r"\bLateUpdate\b",
    r"\bFixedUpdate\b",
    r"\bWaitForSeconds(?:Realtime)?\b",
    r"\bRigidbody\b",
    r"\bGameObject\b",
    r"\bMathf\.",
    r"\bFindObjects?OfType\b",
    r"\bFrameTimingManager\b",
    r"\bProfilerRecorder\b",
    r"\bSetPass\b",
    r"\bDeep Profile\b",
]

# Versions figées à ne pas laisser derrière : la cible est Godot 4.x.
PINS_DE_VERSION = [r"\b4\.7\b", r"\b6\.3\b", r"\b5\.8\b"]


def texte_router() -> str:
    return "\n".join(
        p.read_text(encoding="utf-8") for p in sorted(ROUTER.rglob("*.md"))
    )


def texte_couche_jeu() -> str:
    return "\n".join(
        p.read_text(encoding="utf-8")
        for p in sorted(COUCHE_JEU.rglob("*.md"))
    )


class TestCoucheJeuCuratee(unittest.TestCase):
    def test_la_couche_jeu_contient_exactement_les_skills_gardes(self):
        presents = {p.name for p in COUCHE_JEU.iterdir() if p.is_dir()}
        ecartes = presents - SKILLS_GARDES
        self.assertEqual(
            set(),
            ecartes,
            f"skills écartés encore présents : {sorted(ecartes)}",
        )

    def test_chaque_skill_garde_expose_un_skill_md(self):
        for skill in sorted(SKILLS_GARDES):
            with self.subTest(skill=skill):
                self.assertTrue(
                    (COUCHE_JEU / skill / "SKILL.md").is_file(),
                    f"{skill} n'a pas de SKILL.md",
                )

    def test_aucune_reference_a_un_skill_ecarte(self):
        """Un skill gardé ne doit pas renvoyer vers un skill supprimé.

        La recherche est insensible à la casse : « Platformer » ou « RPG » doivent
        être détectés comme leurs équivalents minuscules.
        """
        for skill in sorted(SKILLS_GARDES):
            for chemin in sorted((COUCHE_JEU / skill).rglob("*.md")):
                texte = chemin.read_text(encoding="utf-8")
                for motif in MOTIFS_SKILLS_ECARTES:
                    with self.subTest(skill=skill, fichier=chemin.name, motif=motif):
                        self.assertIsNone(
                            re.search(motif, texte, flags=re.IGNORECASE),
                            f"{chemin.relative_to(RACINE)} cite encore « {motif} »",
                        )

    def test_aucune_prose_d_un_autre_moteur(self):
        texte = texte_couche_jeu()
        for motif in MOTS_AUTRES_MOTEURS + API_AUTRES_MOTEURS:
            with self.subTest(motif=motif):
                self.assertIsNone(
                    re.search(motif, texte, flags=re.IGNORECASE),
                    f"la Couche jeu cite encore une API/un autre moteur « {motif} »",
                )

    def test_aucun_pin_de_version_fige(self):
        """La cible est Godot 4.x : pas de version d'éditeur figée dans le texte."""
        texte = texte_couche_jeu()
        for motif in PINS_DE_VERSION:
            with self.subTest(motif=motif):
                self.assertIsNone(
                    re.search(motif, texte),
                    f"un pin de version figé traîne : « {motif} »",
                )


class TestRouter(unittest.TestCase):
    def test_le_router_pointe_uniquement_des_skills_gardes(self):
        # Un nom de skill est un identifiant kebab-case entre backticks
        # (`godot-gdscript`, `game-feel`, …). Les chemins (`project.godot`), les
        # commandes (`butler`), les mots du code (`await`) et les clés de
        # frontmatter (`name`) ne sont pas des noms de skill et sont ignorés.
        # Les noms écartés d'un seul mot (platformer, puzzle, …) sont couverts
        # par test_le_router_ne_cite_aucun_skill_ecarte.
        cites = set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", texte_router()))
        skills_connus = {p.name for p in COUCHE_JEU.iterdir() if p.is_dir()}
        inconnu_ou_ecarte = cites - skills_connus
        self.assertEqual(
            set(),
            inconnu_ou_ecarte,
            f"le router cite des skills absents de la Couche jeu : {sorted(inconnu_ou_ecarte)}",
        )

    def test_le_router_ne_cite_aucun_skill_ecarte(self):
        texte = texte_router()
        for motif in MOTIFS_SKILLS_ECARTES:
            with self.subTest(motif=motif):
                self.assertIsNone(
                    re.search(motif, texte, flags=re.IGNORECASE),
                    f"le router cite encore un skill écarté « {motif} »",
                )

    def test_le_router_pointe_les_cles_conservees(self):
        texte = texte_router()
        for skill in sorted(SKILLS_GARDES - {"game-jam"}):
            with self.subTest(skill=skill):
                self.assertIn(skill, texte, f"le router ne pointe pas {skill}")

    def test_game_jam_est_en_reserve_dans_le_router(self):
        """`game-jam` doit être présenté comme réserve, pas comme une clé par défaut.

        Contrôle porté sur le *corps* du router (pas sur la concaténation des
        references, qui masqueraient une requalification) : la section « Réserve »
        doit mentionner `game-jam` ET le qualifier. Un « game-jam est une clé
        normale » doit faire échouer ce test.
        """
        corps = (ROUTER / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("game-jam", corps, "game-jam doit rester dans la Couche jeu")

        section = re.search(
            r"^#{2,3}\s*(?:3c\.)?\s*réserve\b.*?(?=^#{2,3}\s|\Z)",
            corps,
            flags=re.MULTILINE | re.IGNORECASE | re.DOTALL,
        )
        self.assertIsNotNone(
            section, "le corps du router n'a pas de section « Réserve » explicite"
        )
        contenu = section.group(0)
        # On ignore la ligne d'en-tête : c'est la LIGNE qui présente game-jam qui
        # doit porter le qualificatif, sinon « Réserve » dans le titre suffit à
        # faire passer une réqualification en clé normale.
        corps_section = "\n".join(contenu.splitlines()[1:])
        lignes_jam = [
            ligne
            for ligne in corps_section.splitlines()
            if "game-jam" in ligne
        ]
        self.assertTrue(
            lignes_jam, "la section Réserve ne présente pas game-jam"
        )
        restrictif = [
            ligne
            for ligne in lignes_jam
            if re.search(r"réserv|reserve|only|explicite|explicit|on demand", ligne, re.IGNORECASE)
        ]
        self.assertTrue(
            restrictif,
            "la ligne présentant game-jam ne le qualifie pas de réserve : "
            f"{lignes_jam}",
        )

    def test_la_table_des_7_cles_exclut_la_reserve(self):
        """La table de routage compte 7 clés numérotées ; game-jam est la ligne « R »."""
        table = (ROUTER / "references" / "routing-table.md").read_text(encoding="utf-8")
        bloc = re.search(
            r"^##\s*(?:The\s+|Les\s+)?7\s+clés\s*$(.*?)(?=^##\s|\Z)",
            table,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(bloc, "la table « Les 7 clés » est introuvable")
        lignes = [l for l in bloc.group(1).splitlines() if l.strip().startswith("|")]
        numerotees = [l for l in lignes if re.match(r"^\|\s*[1-7]\s*\|", l)]
        self.assertEqual(
            7, len(numerotees), f"la table doit lister 7 clés numérotées : {numerotees}"
        )
        reserve = [l for l in lignes if "game-jam" in l]
        self.assertEqual(1, len(reserve), "game-jam doit apparaître une seule fois")
        self.assertRegex(
            reserve[0],
            r"^\|\s*R\s*\|",
            "game-jam doit être la ligne « R » (réserve), hors des 7 clés numérotées",
        )


if __name__ == "__main__":
    unittest.main()
