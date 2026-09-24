# Mono requis par Godot-MCP

Godot-MCP est un addon C# compilé avec le projet, donc nous exigeons Godot 4.3+ édition mono avec .NET 8 SDK : un build standard GDScript-only ne peut pas compiler l'addon et désactive le pilotage éditeur, qui retombe alors sur le seul fallback CLI headless.
