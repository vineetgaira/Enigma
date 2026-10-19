"""A polished desktop field console for the Enigma I simulator."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .machine import EnigmaMachine
from .rotor import ALPHABET
from .wiring import REFLECTORS, ROTORS

BG = "#171a18"
CHASSIS = "#292b27"
PANEL = "#343630"
PANEL_DARK = "#20231f"
EDGE = "#4a4a3f"
IVORY = "#e8dec8"
MUTED = "#a39b88"
BRASS = "#c6a66b"
BRASS_DARK = "#8f7041"
LAMP = "#d9bb78"
GREEN = "#a6c391"
RED = "#cc8e73"
FONT_SANS = "Noto Sans"
FONT_SERIF = "Noto Serif"
FONT_MONO = "JetBrainsMono Nerd Font"


class EnigmaConsole(tk.Tk):
    """A configurable three-rotor Enigma I desktop application."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Enigma I · Cipher Machine")
        self.geometry("1240x980")
        self.minsize(1000, 760)
        self.configure(bg=BG)
        self.rotor_vars: list[tk.StringVar] = []
        self.position_vars: list[tk.StringVar] = []
        self.ring_vars: list[tk.StringVar] = []
        self.lamp_labels: dict[str, tk.Label] = {}
        self.live_machine: EnigmaMachine | None = None
        self.start_positions = list("AAA")
        self._style()
        self._build()

    def _style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Instrument.TCombobox",
            fieldbackground="#e3d9c3",
            background="#c6a66b",
            foreground="#252720",
            arrowcolor="#252720",
            bordercolor=BRASS_DARK,
            lightcolor=BRASS_DARK,
            darkcolor=BRASS_DARK,
            padding=(8, 6),
            font=(FONT_MONO, 10, "bold"),
        )
        style.configure(
            "Instrument.Vertical.TScrollbar",
            background=PANEL,
            troughcolor=BG,
            bordercolor=BG,
            arrowcolor=BRASS,
            gripcount=0,
        )
        style.map(
            "Instrument.TCombobox",
            fieldbackground=[("readonly", "#e3d9c3")],
            selectbackground=[("readonly", "#e3d9c3")],
            selectforeground=[("readonly", "#252720")],
        )

    def _build(self) -> None:
        self._header()
        viewport = tk.Frame(self, bg=BG)
        viewport.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(viewport, bg=BG, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(
            viewport, orient="vertical", command=self.canvas.yview, style="Instrument.Vertical.TScrollbar"
        )
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.body = tk.Frame(self.canvas, bg=BG)
        self.body_window = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.body.bind("<Configure>", lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfigure(self.body_window, width=event.width))
        self.canvas.bind_all("<MouseWheel>", self._scroll)
        self.canvas.bind_all("<Button-4>", lambda _event: self.canvas.yview_scroll(-3, "units"))
        self.canvas.bind_all("<Button-5>", lambda _event: self.canvas.yview_scroll(3, "units"))
        self._machine_panel()
        self._traffic_panel()
        self._keyboard_panel()
        self._reference_panel()

    def _scroll(self, event: tk.Event) -> None:
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def _header(self) -> None:
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=36, pady=(26, 20))
        left = tk.Frame(header, bg=BG)
        left.pack(side="left", fill="x", expand=True)
        tk.Label(
            left,
            text="CHIFFRIERMASCHINEN A.G.  ·  BERLIN",
            bg=BG,
            fg=BRASS,
            font=(FONT_MONO, 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            left,
            text="Enigma I",
            bg=BG,
            fg=IVORY,
            font=(FONT_SERIF, 30, "bold"),
        ).pack(anchor="w", pady=(2, 0))
        tk.Label(
            left,
            text="THREE-ROTOR ELECTROMECHANICAL CIPHER  /  FIELD SIMULATOR",
            bg=BG,
            fg=MUTED,
            font=(FONT_MONO, 8),
        ).pack(anchor="w", pady=(1, 0))

        seal = tk.Frame(header, bg=CHASSIS, highlightthickness=1, highlightbackground=EDGE)
        seal.pack(side="right", anchor="center", padx=(12, 0))
        tk.Label(seal, text="I", bg=CHASSIS, fg=BRASS, font=(FONT_SERIF, 27, "bold"), width=3).pack(
            side="left", padx=(9, 0), pady=4
        )
        tk.Frame(seal, bg=EDGE, width=1, height=34).pack(side="left", padx=5)
        tk.Label(
            seal,
            text="SERIES\nENIGMA I",
            justify="left",
            bg=CHASSIS,
            fg=IVORY,
            font=(FONT_MONO, 8, "bold"),
        ).pack(side="left", padx=(3, 13), pady=4)

    def _panel(self, parent: tk.Widget, eyebrow: str, title: str = "") -> tuple[tk.Frame, tk.Frame]:
        outer = tk.Frame(parent, bg=CHASSIS, highlightthickness=1, highlightbackground=EDGE)
        head = tk.Frame(outer, bg=CHASSIS)
        head.pack(fill="x", padx=18, pady=(14, 9))
        tk.Label(head, text=eyebrow, bg=CHASSIS, fg=BRASS, font=(FONT_MONO, 8, "bold")).pack(side="left")
        if title:
            tk.Label(head, text=title, bg=CHASSIS, fg=IVORY, font=(FONT_SERIF, 12, "bold")).pack(
                side="right"
            )
        content = tk.Frame(outer, bg=CHASSIS)
        content.pack(fill="both", expand=True, padx=18, pady=(0, 16))
        return outer, content

    def _machine_panel(self) -> None:
        outer, content = self._panel(self.body, "01  /  MACHINE SETTINGS", "Configure the key")
        outer.pack(fill="x", padx=36, pady=(0, 14))

        rotor_deck = tk.Frame(content, bg=PANEL_DARK, highlightthickness=1, highlightbackground=EDGE)
        rotor_deck.pack(fill="x", pady=(0, 13))
        deck_header = tk.Frame(rotor_deck, bg=PANEL_DARK)
        deck_header.pack(fill="x", padx=13, pady=(11, 8))
        tk.Label(deck_header, text="ROTOR BANK", bg=PANEL_DARK, fg=MUTED, font=(FONT_MONO, 8, "bold")).pack(
            side="left"
        )
        self.position_display = tk.Label(
            deck_header,
            text="WINDOWS   A   A   A",
            bg=PANEL_DARK,
            fg=GREEN,
            font=(FONT_MONO, 9, "bold"),
        )
        self.position_display.pack(side="right")

        rotor_row = tk.Frame(rotor_deck, bg=PANEL_DARK)
        rotor_row.pack(fill="x", padx=11, pady=(0, 11))
        rotor_labels = ("LEFT  /  SLOW", "MIDDLE", "RIGHT  /  FAST")
        for index, label in enumerate(rotor_labels):
            rotor_row.columnconfigure(index, weight=1, uniform="rotors")
            self._rotor_card(rotor_row, index, label).grid(
                row=0, column=index, sticky="ew", padx=(0 if index == 0 else 5, 0 if index == 2 else 5)
            )
        lower = tk.Frame(content, bg=CHASSIS)
        lower.pack(fill="x")
        reflector_box = tk.Frame(lower, bg=PANEL, highlightthickness=1, highlightbackground=EDGE)
        reflector_box.pack(side="left", fill="y", padx=(0, 10))
        tk.Label(reflector_box, text="REFLECTOR", bg=PANEL, fg=MUTED, font=(FONT_MONO, 8, "bold")).pack(
            anchor="w", padx=12, pady=(10, 5)
        )
        self.reflector_var = tk.StringVar(value="B")
        reflector_combo = ttk.Combobox(
            reflector_box,
            textvariable=self.reflector_var,
            values=("B", "C"),
            state="readonly",
            width=6,
            style="Instrument.TCombobox",
        )
        reflector_combo.pack(anchor="w", padx=12, pady=(0, 10))
        reflector_combo.bind("<<ComboboxSelected>>", lambda _event: self._invalidate_live_machine())

        plug_box = tk.Frame(lower, bg=PANEL, highlightthickness=1, highlightbackground=EDGE)
        plug_box.pack(side="left", fill="both", expand=True)
        plug_head = tk.Frame(plug_box, bg=PANEL)
        plug_head.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(plug_head, text="PLUGBOARD  /  STECKERBRETT", bg=PANEL, fg=MUTED,
                 font=(FONT_MONO, 8, "bold")).pack(side="left")
        tk.Label(plug_head, text="UP TO 13 PAIRS", bg=PANEL, fg=BRASS_DARK, font=(FONT_MONO, 7)).pack(side="right")
        plug_controls = tk.Frame(plug_box, bg=PANEL)
        plug_controls.pack(fill="x", padx=12, pady=(0, 10))
        self.plugboard_var = tk.StringVar()
        self.plugboard_entry = tk.Entry(
            plug_controls,
            textvariable=self.plugboard_var,
            bg="#e3d9c3",
            fg="#252720",
            insertbackground="#252720",
            relief="flat",
            font=(FONT_MONO, 11, "bold"),
            width=27,
        )
        self.plugboard_entry.pack(side="left", ipady=6, ipadx=7)
        tk.Label(plug_controls, text="Pairs like  AB  CD  EF", bg=PANEL, fg=MUTED,
                 font=(FONT_SANS, 8)).pack(side="left", padx=12)
        self.pair_badges = tk.Frame(plug_box, bg=PANEL)
        self.pair_badges.pack(fill="x", padx=12, pady=(0, 10))
        self.plugboard_var.trace_add("write", lambda *_: self._plugboard_changed())
        self._update_pair_badges()

    def _rotor_card(self, parent: tk.Widget, index: int, label: str) -> tk.Frame:
        card = tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=EDGE)
        head = tk.Frame(card, bg=PANEL)
        head.pack(fill="x", padx=12, pady=(10, 6))
        tk.Label(head, text=label, bg=PANEL, fg=MUTED, font=(FONT_MONO, 7, "bold")).pack(side="left")
        self.notch_labels = getattr(self, "notch_labels", [])
        notch = tk.Label(head, text="NOTCH · Q", bg=PANEL, fg=BRASS, font=(FONT_MONO, 7))
        notch.pack(side="right")
        self.notch_labels.append(notch)

        self.rotor_vars.append(tk.StringVar(value=("I", "II", "III")[index]))
        rotor_combo = ttk.Combobox(
            card,
            textvariable=self.rotor_vars[index],
            values=tuple(ROTORS),
            state="readonly",
            width=9,
            style="Instrument.TCombobox",
        )
        rotor_combo.pack(anchor="w", padx=12)
        rotor_combo.bind("<<ComboboxSelected>>", lambda _event, i=index: self._rotor_changed(i))

        controls = tk.Frame(card, bg=PANEL)
        controls.pack(fill="x", padx=12, pady=(9, 11))
        self.position_vars.append(tk.StringVar(value="A"))
        self.ring_vars.append(tk.StringVar(value="A"))
        self._letter_dial(
            controls, "WINDOW", self.position_vars[index], on_select=lambda i=index: self._window_changed(i)
        ).pack(side="left", fill="x", expand=True)
        tk.Frame(controls, bg=EDGE, width=1).pack(side="left", fill="y", padx=9)
        self._letter_dial(controls, "RING", self.ring_vars[index], on_select=self._invalidate_live_machine).pack(
            side="left", fill="x", expand=True
        )
        return card

    def _letter_dial(self, parent: tk.Widget, label: str, variable: tk.StringVar, on_select) -> tk.Frame:
        group = tk.Frame(parent, bg=PANEL)
        tk.Label(group, text=label, bg=PANEL, fg=MUTED, font=(FONT_MONO, 7)).pack(anchor="w")
        combo = ttk.Combobox(
            group,
            textvariable=variable,
            values=tuple(ALPHABET),
            state="readonly",
            width=3,
            style="Instrument.TCombobox",
            justify="center",
        )
        combo.pack(anchor="w", pady=(3, 0))
        combo.bind("<<ComboboxSelected>>", lambda _event: on_select())
        return group

    def _window_changed(self, index: int) -> None:
        self.start_positions[index] = self.position_vars[index].get()
        self._invalidate_live_machine()

    def _rotor_changed(self, index: int) -> None:
        name = self.rotor_vars[index].get()
        self.notch_labels[index].configure(text=f"NOTCH · {ROTORS[name][1]}")
        self._invalidate_live_machine()

    def _plugboard_changed(self) -> None:
        self._update_pair_badges()
        self._invalidate_live_machine()

    def _update_pair_badges(self) -> None:
        if not hasattr(self, "pair_badges"):
            return
        for child in self.pair_badges.winfo_children():
            child.destroy()
        pairs = self.plugboard_var.get().upper().split()
        if not pairs:
            tk.Label(self.pair_badges, text="No connections · direct signal", bg=PANEL, fg=MUTED,
                     font=(FONT_SANS, 8, "italic")).pack(side="left")
            return
        for pair in pairs[:13]:
            badge = tk.Label(self.pair_badges, text=pair, bg="#252720", fg=IVORY,
                             font=(FONT_MONO, 8, "bold"), padx=8, pady=3)
            badge.pack(side="left", padx=(0, 5))

    def _traffic_panel(self) -> None:
        outer, content = self._panel(self.body, "02  /  MESSAGE TRAFFIC", "Encrypt · decrypt · inspect")
        outer.pack(fill="both", expand=True, padx=36, pady=(0, 14))

        text_columns = tk.Frame(content, bg=CHASSIS)
        text_columns.pack(fill="both", expand=True)
        for index in range(2):
            text_columns.columnconfigure(index, weight=1, uniform="traffic")
        input_panel, self.input_text = self._message_box(text_columns, "INPUT  /  PLAINTEXT OR CIPHERTEXT", "#e3d9c3", "#252720")
        input_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        self.input_text.bind("<KeyRelease>", lambda _event: self._invalidate_live_machine())
        self.input_text.bind("<<Paste>>", lambda _event: self._invalidate_live_machine())
        output_panel, self.output_text = self._message_box(text_columns, "OUTPUT  /  TRANSFORMED MESSAGE", PANEL_DARK, GREEN, disabled=True)
        output_panel.grid(row=0, column=1, sticky="nsew", padx=(7, 0))
        text_columns.rowconfigure(0, weight=1)

        actions = tk.Frame(content, bg=CHASSIS)
        actions.pack(fill="x", pady=(11, 0))
        self._button(actions, "RUN MACHINE", self.process_message, primary=True).pack(side="left")
        self._button(actions, "COPY OUTPUT", self.copy_output).pack(side="left", padx=(8, 0))
        self._button(actions, "LOAD OUTPUT AS INPUT", self.load_output).pack(side="left", padx=(8, 0))
        self._button(actions, "CLEAR", self.clear_messages).pack(side="left", padx=(8, 0))
        self._button(actions, "RESTORE START", self.reset_windows).pack(side="right")
        self.status = tk.Label(
            content,
            text="READY  ·  LETTERS STEP THE ROTORS; PUNCTUATION PASSES THROUGH",
            bg=CHASSIS,
            fg=MUTED,
            font=(FONT_MONO, 8),
            anchor="w",
        )
        self.status.pack(fill="x", pady=(10, 0))

    def _message_box(
        self, parent: tk.Widget, caption: str, background: str, foreground: str, disabled: bool = False
    ) -> tuple[tk.Frame, tk.Text]:
        container = tk.Frame(parent, bg=CHASSIS)
        container.pack_propagate(False)
        container.configure(height=155)
        tk.Label(container, text=caption, bg=CHASSIS, fg=MUTED, font=(FONT_MONO, 7, "bold")).pack(
            anchor="w", pady=(0, 5)
        )
        editor = tk.Frame(container, bg=background)
        editor.pack(fill="both", expand=True)
        text = tk.Text(
            editor,
            height=5,
            wrap="word",
            bg=background,
            fg=foreground,
            insertbackground=foreground,
            selectbackground=BRASS_DARK,
            selectforeground=IVORY,
            relief="flat",
            padx=12,
            pady=10,
            font=(FONT_MONO, 11),
            undo=not disabled,
            state="disabled" if disabled else "normal",
            borderwidth=0,
        )
        text.pack(side="left", fill="both", expand=True)
        text_scroll = ttk.Scrollbar(
            editor,
            orient="vertical",
            command=text.yview,
            style="Instrument.Vertical.TScrollbar",
        )
        text_scroll.pack(side="right", fill="y")
        text.configure(yscrollcommand=text_scroll.set)
        text.bind("<MouseWheel>", lambda event, widget=text: self._scroll_text(event, widget))
        text.bind("<Button-4>", lambda _event, widget=text: self._scroll_text_linux(widget, -1))
        text.bind("<Button-5>", lambda _event, widget=text: self._scroll_text_linux(widget, 1))
        return container, text

    @staticmethod
    def _scroll_text(event: tk.Event, widget: tk.Text) -> str:
        widget.yview_scroll(int(-event.delta / 120), "units")
        return "break"

    @staticmethod
    def _scroll_text_linux(widget: tk.Text, direction: int) -> str:
        widget.yview_scroll(direction * 3, "units")
        return "break"

    def _button(self, parent: tk.Widget, label: str, command, primary: bool = False) -> tk.Button:
        bg = BRASS if primary else PANEL
        fg = "#20221e" if primary else IVORY
        return tk.Button(
            parent,
            text=label,
            command=command,
            bg=bg,
            fg=fg,
            activebackground="#d9bd88" if primary else "#45473f",
            activeforeground=fg,
            relief="flat",
            bd=0,
            padx=14,
            pady=9,
            cursor="hand2",
            font=(FONT_SANS, 8, "bold"),
        )

    def _keyboard_panel(self) -> None:
        outer, content = self._panel(self.body, "03  /  KEYBOARD & LAMPBOARD", "German QWERTZ layout")
        outer.pack(fill="x", padx=36, pady=(0, 14))
        tk.Label(
            content,
            text="The lampboard shows the last output letter. Select a key to process one letter at the current rotor position.",
            bg=CHASSIS,
            fg=MUTED,
            font=(FONT_SANS, 8),
        ).pack(anchor="w", pady=(0, 10))
        self.lamp_labels = {}
        self._key_buttons: dict[str, tk.Button] = {}
        for row_letters in ("QWERTZUIO", "ASDFGHJK", "PYXCVBNML"):
            line = tk.Frame(content, bg=CHASSIS)
            line.pack(pady=3)
            for letter in row_letters:
                key_column = tk.Frame(line, bg=CHASSIS)
                key_column.pack(side="left", padx=3)
                lamp = tk.Label(
                    key_column,
                    text="·",
                    width=3,
                    height=1,
                    bg=PANEL_DARK,
                    fg="#77776d",
                    relief="flat",
                    font=(FONT_MONO, 9, "bold"),
                )
                lamp.pack(pady=(0, 2))
                self.lamp_labels[letter] = lamp
                key = tk.Button(
                    key_column,
                    text=letter,
                    width=3,
                    height=1,
                    bg=PANEL,
                    fg=IVORY,
                    activebackground=BRASS,
                    activeforeground=BG,
                    relief="raised",
                    bd=2,
                    padx=5,
                    pady=5,
                    cursor="hand2",
                    font=(FONT_MONO, 10, "bold"),
                    command=lambda char=letter: self.press_key(char),
                )
                key.pack()
                self._key_buttons[letter] = key

    def _reference_panel(self) -> None:
        outer, content = self._panel(self.body, "04  /  FIELD NOTES", "A signal, reflected")
        outer.pack(fill="x", padx=36, pady=(0, 24))
        columns = tk.Frame(content, bg=CHASSIS)
        columns.pack(fill="x")
        for index in range(3):
            columns.columnconfigure(index, weight=1, uniform="notes")
        notes = (
            ("SIGNAL PATH", "Keyboard → plugboard → right, middle, left rotors → reflector → return path → lampboard."),
            ("ROTOR ACTION", "The fast rotor advances with every key. Its notch advances the middle rotor; the middle notch advances the left rotor and creates the double-step."),
            ("RECIPROCAL CIPHER", "The reflector makes encryption and decryption the same operation. Use identical settings and starting windows."),
        )
        for index, (heading, body) in enumerate(notes):
            block = tk.Frame(columns, bg=CHASSIS)
            block.grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 12, 12 if index < 2 else 0))
            tk.Label(block, text=heading, bg=CHASSIS, fg=BRASS, font=(FONT_MONO, 8, "bold")).pack(anchor="w")
            tk.Label(block, text=body, bg=CHASSIS, fg=IVORY, justify="left", wraplength=290,
                     font=(FONT_SANS, 8)).pack(anchor="w", pady=(5, 0))
        detail = tk.Frame(content, bg=PANEL_DARK)
        detail.pack(fill="x", pady=(13, 0))
        rotor_names = tuple(ROTORS)
        rotor_rows = (rotor_names[:3], rotor_names[3:])
        for names in rotor_rows:
            rotor_notes = "     ·     ".join(
                f"{name}  {ROTORS[name][0]}  /  notch {ROTORS[name][1]}" for name in names
            )
            tk.Label(detail, text=rotor_notes, bg=PANEL_DARK, fg=MUTED, font=(FONT_MONO, 7)).pack(
                anchor="w", padx=11, pady=(7, 0)
            )
        reflector_notes = "     ·     ".join(
            f"Reflector {name}: {wiring}" for name, wiring in REFLECTORS.items()
        )
        tk.Label(detail, text=reflector_notes, bg=PANEL_DARK, fg=MUTED, font=(FONT_MONO, 7)).pack(
            anchor="w", padx=11, pady=(5, 8)
        )

    def _machine(self) -> EnigmaMachine:
        return EnigmaMachine(
            rotors=tuple(var.get() for var in self.rotor_vars),
            positions="".join(var.get() for var in self.position_vars),
            ring_settings="".join(var.get() for var in self.ring_vars),
            reflector=self.reflector_var.get(),
            plugboard=self.plugboard_var.get(),
        )

    def _invalidate_live_machine(self) -> None:
        self.live_machine = None

    def process_message(self) -> None:
        message = self.input_text.get("1.0", "end-1c")
        try:
            machine = self._machine()
            result = machine.process(message)
        except ValueError as exc:
            messagebox.showerror("Invalid machine settings", str(exc), parent=self)
            self.status.configure(text=f"CHECK SETTINGS  ·  {exc}", fg=RED)
            return
        self._set_output(result)
        self.live_machine = machine
        self._show_positions(machine.positions)
        final_letter = next((c for c in reversed(result) if c in ALPHABET), "")
        self._light(final_letter)
        count = sum(c.isascii() and c.upper() in ALPHABET for c in message)
        self.status.configure(text=f"COMPLETE  ·  {count} LETTERS STEPPED", fg=GREEN)

    def press_key(self, letter: str) -> None:
        try:
            if self.live_machine is None:
                self.live_machine = self._machine()
            result = self.live_machine.process(letter)
        except ValueError as exc:
            messagebox.showerror("Invalid machine settings", str(exc), parent=self)
            self.status.configure(text=f"CHECK SETTINGS  ·  {exc}", fg=RED)
            return
        self.input_text.insert("end", letter)
        self._append_output(result)
        self._show_positions(self.live_machine.positions)
        self._light(result)
        self.status.configure(text=f"KEY {letter}  →  LAMP {result}  ·  LIVE KEY MODE", fg=GREEN)

    def _set_output(self, text: str) -> None:
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.configure(state="disabled")

    def _append_output(self, text: str) -> None:
        self.output_text.configure(state="normal")
        self.output_text.insert("end", text)
        self.output_text.configure(state="disabled")

    def _show_positions(self, positions: str) -> None:
        self.position_display.configure(text=f"WINDOWS   {'   '.join(positions)}")
        for variable, letter in zip(self.position_vars, positions, strict=True):
            variable.set(letter)

    def _light(self, letter: str) -> None:
        for key, lamp in self.lamp_labels.items():
            active = key == letter
            lamp.configure(bg=LAMP if active else PANEL_DARK, fg="#332c1e" if active else "#77776d")

    def copy_output(self) -> None:
        output = self.output_text.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(output)
        self.status.configure(text="OUTPUT COPIED TO CLIPBOARD", fg=GREEN)

    def load_output(self) -> None:
        output = self.output_text.get("1.0", "end-1c")
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", output)
        self._invalidate_live_machine()
        self.status.configure(text="OUTPUT LOADED AS INPUT  ·  RESET WINDOWS TO REUSE THE ORIGINAL KEY", fg=MUTED)

    def reset_windows(self) -> None:
        self.live_machine = None
        positions = "".join(self.start_positions)
        self._show_positions(positions)
        self._light("")
        self.status.configure(text=f"STARTING WINDOWS RESTORED TO {positions}", fg=MUTED)

    def clear_messages(self) -> None:
        self.live_machine = None
        self.input_text.delete("1.0", "end")
        self._set_output("")
        self._light("")
        self.status.configure(text="MESSAGE BUFFERS CLEARED", fg=MUTED)


def main() -> None:
    """Launch the Enigma I field console."""
    EnigmaConsole().mainloop()


if __name__ == "__main__":
    main()
