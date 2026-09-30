import flet as ft


async def main(page: ft.Page):
    # ---------- 页面基础设置（桌面端模拟手机窗口） ----------
    page.title = "Flet 手机应用演示"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    # 仅桌面端设置窗口尺寸，移动端/APK 忽略
    try:
        page.window.width = 420
        page.window.height = 800
    except Exception:
        pass

    # ---------- 全局状态（跨页面共享数据） ----------
    user = {
        "name": "",
        "gender": "男",
        "city": "",
        "hobbies": [],
        "notify": True,
        "volume": 50,
    }

    def show_snack(msg: str, ok: bool = True):
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(msg, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_600 if ok else ft.Colors.RED_600,
                duration=2000,
            )
        )

    # ============================================================
    # 首页：文本输入 + 各种按钮
    # ============================================================
    echo = ft.Text("输入预览：（空）", size=14, color=ft.Colors.GREY_600)

    name_field = ft.TextField(
        label="用户名",
        hint_text="请输入用户名",
        prefix_icon=ft.Icons.PERSON,
        border=ft.OutlineInputBorder(border_radius=12),
    )

    pwd_field = ft.TextField(
        label="密码",
        hint_text="请输入密码",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        border=ft.OutlineInputBorder(border_radius=12),
    )

    def text_changed(e):
        echo.value = f"输入预览：{name_field.value or '（空）'}"
        page.update()

    name_field.on_change = text_changed

    def login(e):
        if not name_field.value or not pwd_field.value:
            show_snack("用户名和密码不能为空！", ok=False)
            return
        user["name"] = name_field.value
        show_snack(f"欢迎你，{name_field.value}！")

    def clear_all(e):
        name_field.value = ""
        pwd_field.value = ""
        echo.value = "输入预览：（空）"
        page.update()

    # 点击计数
    count = 0
    count_text = ft.Text("点击次数：0", size=16, weight=ft.FontWeight.BOLD)

    def add_count(e):
        nonlocal count
        count += 1
        count_text.value = f"点击次数：{count}"
        page.update()

    def reset_count(e=None):
        nonlocal count
        count = 0
        count_text.value = "点击次数：0"
        page.update()

    home_view = ft.Column(
        [
            ft.Container(
                ft.Text("① 文本输入 & 按钮", size=20, weight=ft.FontWeight.BOLD),
                margin=ft.Margin(top=12),
            ),
            echo,
            name_field,
            pwd_field,
            ft.Row(
                [
                    ft.FilledButton("登录", icon=ft.Icons.LOGIN, on_click=login, expand=True),
                    ft.OutlinedButton("清空", icon=ft.Icons.CLEAR, on_click=clear_all, expand=True),
                ],
                spacing=10,
            ),
            ft.Divider(),
            ft.Text("② 按钮点击", size=20, weight=ft.FontWeight.BOLD),
            count_text,
            ft.Row(
                [
                    ft.IconButton(
                        ft.Icons.ADD,
                        icon_color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.INDIGO,
                        on_click=add_count,
                    ),
                    ft.Button("点我加一", on_click=add_count),
                    ft.FilledTonalButton("重置", on_click=reset_count),
                ]
            ),
            ft.Divider(),
            ft.Text("③ 界面切换", size=20, weight=ft.FontWeight.BOLD),
            ft.Button(
                "查看个人资料 →",
                icon=ft.Icons.ARROW_FORWARD,
                on_click=lambda e: page.navigate("/detail"),
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=14,
        expand=True,
    )

    # ============================================================
    # 控件页：下拉框 / 复选框 / 单选 / 开关 / 滑块
    # ============================================================
    summary = ft.Text(size=14, color=ft.Colors.GREY_800)

    city_dd = ft.Dropdown(
        label="所在城市",
        hint_text="请选择城市",
        leading_icon=ft.Icons.LOCATION_CITY,
        options=[
            ft.DropdownOption("北京"),
            ft.DropdownOption("上海"),
            ft.DropdownOption("广州"),
            ft.DropdownOption("深圳"),
        ],
        on_select=lambda e: update_summary(),
    )

    gender_group = ft.RadioGroup(
        value="男",
        content=ft.Row(
            [ft.Radio(value="男", label="男"), ft.Radio(value="女", label="女")]
        ),
        on_change=lambda e: update_summary(),
    )

    hobby_boxes = [
        ft.Checkbox(label=h, on_change=lambda e: update_summary())
        for h in ["阅读", "运动", "音乐"]
    ]

    notify_sw = ft.Switch(label="消息通知", value=True, on_change=lambda e: update_summary())

    vol_slider = ft.Slider(
        min=0, max=100, divisions=10, label="{value}%", value=50,
        on_change=lambda e: update_summary(),
    )

    def update_summary():
        user["gender"] = gender_group.value
        user["city"] = city_dd.value or ""
        user["hobbies"] = [cb.label for cb in hobby_boxes if cb.value]
        user["notify"] = notify_sw.value
        user["volume"] = int(vol_slider.value)
        summary.value = (
            f"性别：{user['gender']}    城市：{user['city'] or '未选择'}\n"
            f"爱好：{'、'.join(user['hobbies']) or '无'}\n"
            f"通知：{'开' if user['notify'] else '关'}    音量：{user['volume']}%"
        )
        page.update()

    def submit(e):
        if not city_dd.value:
            show_snack("请先选择一个城市！", ok=False)
            return
        update_summary()
        page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("提交成功"),
                content=ft.Text(
                    f"{user['gender']}性朋友，来自{user['city']}\n"
                    f"爱好：{'、'.join(user['hobbies']) or '无'}"
                ),
                actions=[
                    ft.TextButton("好的", on_click=lambda e: page.pop_dialog()),
                    ft.TextButton(
                        "查看资料页",
                        on_click=lambda e: (page.pop_dialog(), page.navigate("/detail")),
                    ),
                ],
            )
        )

    controls_view = ft.Column(
        [
            ft.Container(
                ft.Text("④ 选择控件", size=20, weight=ft.FontWeight.BOLD),
                margin=ft.Margin(top=12),
            ),
            city_dd,
            ft.Text("性别：", size=15),
            gender_group,
            ft.Text("爱好：", size=15),
            ft.Row(hobby_boxes, spacing=10),
            notify_sw,
            ft.Text("音量：", size=15),
            vol_slider,
            ft.Divider(),
            summary,
            ft.FilledButton("提交选择", icon=ft.Icons.CHECK, on_click=submit, expand=True),
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=14,
        expand=True,
    )

    # ============================================================
    # 详情页：展示提交的数据（通过路由切换到这里）
    # ============================================================
    def build_detail_view():
        rows = [
            ("用户名", user["name"] or "未填写"),
            ("性别", user["gender"]),
            ("城市", user["city"] or "未选择"),
            ("爱好", "、".join(user["hobbies"]) or "无"),
            ("消息通知", "开" if user["notify"] else "关"),
            ("音量", f"{user['volume']}%"),
        ]
        return ft.View(
            route="/detail",
            appbar=ft.AppBar(
                title=ft.Text("个人资料"),
                bgcolor=ft.Colors.INDIGO,
                color=ft.Colors.WHITE,
            ),
            controls=[
                ft.Card(
                    content=ft.Container(
                        ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color=ft.Colors.INDIGO),
                                    title=ft.Text("我的资料", weight=ft.FontWeight.BOLD),
                                ),
                                ft.Divider(height=1),
                                *[
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.INFO_OUTLINE, size=18),
                                        title=ft.Text(k),
                                        trailing=ft.Text(v, weight=ft.FontWeight.BOLD),
                                    )
                                    for k, v in rows
                                ],
                            ],
                            spacing=0,
                        )
                    )
                ),
                ft.FilledTonalButton("← 返回首页", on_click=lambda e: page.navigate("/")),
            ],
            spacing=16,
            padding=16,
            scroll=ft.ScrollMode.AUTO,
        )

    # ============================================================
    # 底部导航栏（手机 App 风格）
    # ============================================================
    tab_content = ft.Column([home_view], expand=True)

    def nav_changed(e):
        idx = e.control.selected_index
        tab_content.controls = [home_view if idx == 0 else controls_view]
        update_summary()
        page.update()

    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="首页"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.WIDGETS_OUTLINED, selected_icon=ft.Icons.WIDGETS, label="控件"
            ),
        ],
        on_change=nav_changed,
    )

    main_view = ft.View(
        route="/",
        controls=[tab_content],
        navigation_bar=nav_bar,
    )

    # ---------- 路由：实现界面切换 ----------
    def route_change(e=None):
        page.views.clear()
        page.views.append(main_view)
        if page.route == "/detail":
            page.views.append(build_detail_view())
        page.update()

    def view_pop(e):
        page.navigate("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    update_summary()
    route_change()


if __name__ == "__main__":
    (ft.run if hasattr(ft, "run") else ft.app)(main)
