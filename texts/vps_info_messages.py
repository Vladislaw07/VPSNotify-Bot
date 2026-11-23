from string import Template

VPS_ADDED_TEXT = """✅ <b>VPS успішно додано!</b>

Я нагадаю вам за день до завершення оренди.

Список серверів: <b>/list_vps</b>"""

VPS_INFO_TEXT = Template("""
<b>🖥 $project_name</b>

🌐 IP: <code>$ip</code>
👤 Логін: <code>$login</code>
🔑 Пароль: <code>$password</code>
📅 Оренда до: <i>$rent_end</i>
""")

VPS_DELETE_TEXT = Template("""
⚠️ Ви впевнені, що хочете видалити дані про VPS «<b>$project_name</b>»?

Видалені дані неможливо відновити.
""")

VPS_DELETED_TEXT = """✅ Дані про VPS успішно видалено."""