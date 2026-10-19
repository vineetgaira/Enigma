"""Desktop field console for the Enigma I simulator."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .machine import EnigmaMachine
from .rotor import ALPHABET


INK = "#e8d9b5"
MUTED = "#9c947e"
PANEL = "#252923"
BACKGROUND = "#171b18"
BRASS = "#c39a55"
GREEN = "#91bb77"


class EnigmaConsole(tk.Tk):
    """A configurable desktop Enigma console with live lampboard feedback."""

    def __init__(self) -> None:
        super().__init__()
        self.title("ENIGMA I  /  FIELD CIPHER CONSOLE")
        self.geometry("1080x850")
        self.minsize(900, 720)
        self.configure(bg=BACKGROUND)
        self._style()
        self._build()

    def _style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground="#d4c9ad", background="#d4c9ad", foreground="#171b18")
        style.map("TCombobox", fieldbackground=[("readonly", "#d4c9ad")])
        style.configure("TButton", font=("TkDefaultFont", 10, "bold"), padding=(12, 8))

    def _build(self) -> None:
        top = tk.Frame(self, bg=BACKGROUND)
        top.pack(fill="x", padx=28, pady=(22, 12))
        tk.Label(top, text="SIGNAL CORPS  •  FIELD EQUIPMENT", bg=BACKGROUND, fg=BRASS,
                 font=("TkFixedFont", 10, "bold")).pack(anchor="w")
        tk.Label(top, text="ENIGMA  I", bg=BACKGROUND, fg=INK,
                 font=("TkDefaultFont", 28, "bold")).pack(anchor="w", pady=(4, 0))
        tk.Label(top, text="THREE-ROTOR CIPHER MACHINE  /  SIMULATION CONSOLE",
                 bg=BACKGROUND, fg=MUTED, font=("TkFixedFont", 9)).pack(anchor="w", pady=(1, 0))

        self._settings()
        self._lamps()
        self._message_panel()
        self._reference()

    def _section(self, parent: tk.Widget, title: str) -> tk.Frame:
        frame = tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground="#474638")
        tk.Label(frame, text=title, bg=PANEL, fg=BRASS, font=("TkFixedFont", 10, "bold")).pack(
            anchor="w", padx=14, pady=(12, 7))
        return frame

    def _settings(self) -> None:
        frame = self._section(self, "01  /  MACHINE CONFIGURATION")
        frame.pack(fill="x", padx=28, pady=8)
        controls = tk.Frame(frame, bg=PANEL)
        controls.pack(fill="x", padx=14, pady=(0, 13))
        self.rotor_vars: list[tk.StringVar] = []
        self.position_vars: list[tk.StringVar] = []
        self.ring_vars: list[tk.StringVar] = []
        rotor_names = ("I", "II", "III", "IV", "V")
        for i, label in enumerate(("LEFT ROTOR", "MIDDLE ROTOR", "RIGHT ROTOR")):
            col = tk.Frame(controls, bg=PANEL)
            col.grid(row=0, column=i, sticky="ew", padx=(0, 14))
            tk.Label(col, text=label, bg=PANEL, fg=MUTED, font=("TkFixedFont", 8)).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
            rv = tk.StringVar(value=("I", "II", "III")[i]); self.rotor_vars.append(rv)
            ttk.Combobox(col, textvariable=rv, values=rotor_names, state="readonly", width=8).grid(row=1, column=0, sticky="w")
            pv = tk.StringVar(value="A"); self.position_vars.append(pv)
            self._letter_entry(col, pv, 1, 1, "WINDOW")
            gv = tk.StringVar(value="A"); self.ring_vars.append(gv)
            self._letter_entry(col, gv, 2, 1, "RING")
        controls.columnconfigure((0, 1, 2), weight=1)
        tk.Label(controls, text="REFLECTOR", bg=PANEL, fg=MUTED, font=("TkFixedFont", 8)).grid(row=0, column=3, sticky="w", padx=(2, 0))
        self.reflector_var = tk.StringVar(value="B")
        ttk.Combobox(controls, textvariable=self.reflector_var, values=("B", "C"), state="readonly", width=5).grid(row=1, column=3, sticky="w", padx=(2, 0))
        tk.Label(controls, text="PLUGBOARD PAIRS", bg=PANEL, fg=MUTED, font=("TkFixedFont", 8)).grid(row=0, column=4, sticky="w", padx=(12, 0))
        self.plugboard_var = tk.StringVar()
        tk.Entry(controls, textvariable=self.plugboard_var, width=19, bg="#d4c9ad", fg="#171b18", relief="flat", font=("TkFixedFont", 11)).grid(row=1, column=4, sticky="w", padx=(12, 0))
        tk.Label(controls, text="e.g. AB CD EF  •  max 13 pairs", bg=PANEL, fg=MUTED, font=("TkDefaultFont", 8)).grid(row=2, column=4, sticky="w", padx=(12, 4), pady=(4, 0))

    def _letter_entry(self, parent: tk.Widget, var: tk.StringVar, row: int, column: int, title: str) -> None:
        cell = tk.Frame(parent, bg=PANEL)
        cell.grid(row=row, column=column, padx=(8, 0), sticky="w")
        tk.Label(cell, text=title, bg=PANEL, fg=MUTED, font=("TkFixedFont", 7)).pack(side="left", padx=(0, 4))
        entry = tk.Entry(cell, textvariable=var, width=2, justify="center", bg="#171b18", fg=INK,
                         insertbackground=INK, relief="flat", font=("TkFixedFont", 12, "bold"))
        entry.pack(side="left")
        var.trace_add("write", lambda *_args, v=var: self._normalize_letter(v))

    @staticmethod
    def _normalize_letter(var: tk.StringVar) -> None:
        value = var.get().upper()
        value = next((letter for letter in value if letter in ALPHABET), "A")
        if var.get() != value:
            var.set(value)

    def _lamps(self) -> None:
        frame = self._section(self, "02  /  LAMPBOARD   •   LAST OUTPUT LETTER")
        frame.pack(fill="x", padx=28, pady=8)
        board = tk.Frame(frame, bg=PANEL)
        board.pack(padx=14, pady=(0, 12))
        self.lamp_labels: dict[str, tk.Label] = {}
        for row, letters in enumerate(("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM")):
            line = tk.Frame(board, bg=PANEL)
            line.pack(pady=3)
            for letter in letters:
                lamp = tk.Label(line, text=letter, width=3, height=1, bg="#353a32", fg="#777665",
                                font=("TkFixedFont", 13, "bold"), relief="ridge", bd=2, padx=3, pady=5)
                lamp.pack(side="left", padx=3)
                self.lamp_labels[letter] = lamp
        self.position_display = tk.Label(frame, text="ROTOR WINDOWS     A   A   A", bg=PANEL, fg=GREEN,
                                          font=("TkFixedFont", 13, "bold"))
        self.position_display.pack(pady=(0, 13))

    def _message_panel(self) -> None:
        frame = self._section(self, "03  /  MESSAGE TRAFFIC")
        frame.pack(fill="both", expand=True, padx=28, pady=8)
        body = tk.Frame(frame, bg=PANEL)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 10))
        self.input_text = tk.Text(body, height=4, wrap="word", bg="#d4c9ad", fg="#171b18", insertbackground="#171b18",
                                  relief="flat", padx=10, pady=8, font=("TkFixedFont", 11))
        self.input_text.pack(fill="x", pady=(0, 7))
        self.input_text.insert("1.0", "TYPE OR PASTE YOUR MESSAGE HERE")
        self.output_text = tk.Text(body, height=4, wrap="word", bg="#171b18", fg=GREEN, relief="flat", padx=10, pady=8,
                                   font=("TkFixedFont", 11), state="disabled")
        self.output_text.pack(fill="both", expand=True)
        actions = tk.Frame(body, bg=PANEL)
        actions.pack(fill="x", pady=(8, 0))
        tk.Button(actions, text="PROCESS MESSAGE", command=self.process_message, bg=BRASS, fg="#171b18",
                  activebackground="#d7b46e", relief="flat", font=("TkDefaultFont", 10, "bold"), padx=14, pady=7).pack(side="left")
        tk.Button(actions, text="RESET WINDOWS", command=self.reset_windows, bg="#3d4138", fg=INK,
                  activebackground="#55594d", relief="flat", padx=12, pady=7).pack(side="left", padx=7)
        tk.Button(actions, text="CLEAR", command=self.clear_messages, bg="#3d4138", fg=INK,
                  activebackground="#55594d", relief="flat", padx=12, pady=7).pack(side="left")
        self.status = tk.Label(actions, text="READY  /  LETTERS STEP ROTORS; SPACES AND PUNCTUATION PASS THROUGH", bg=PANEL,
                               fg=MUTED, font=("TkFixedFont", 8), anchor="e")
        self.status.pack(side="right", fill="x", expand=True, padx=(8, 0))

    def _reference(self) -> None:
        frame = self._section(self, "04  /  HOW THE MACHINE WORKS")
        frame.pack(fill="x", padx=28, pady=(8, 20))
        copy = (
            "KEYBOARD → PLUGBOARD → 3 ROTORS → REFLECTOR → ROTORS BACK → PLUGBOARD → LAMPBOARD\n"
            "Each letter advances the right rotor. At a notch, the neighboring rotor turns; the middle rotor can double-step.\n"
            "A reflector sends the signal back through the rotors, making the same settings work for encryption and decryption.\n"
            "Window letters set the starting position. Ring letters offset the wiring. Choose three distinct rotors (I–V)."
        )
        tk.Label(frame, text=copy, justify="left", anchor="w", bg=PANEL, fg=INK,
                 font=("TkDefaultFont", 9), padx=14, pady=(0, 13)).pack(fill="x")

    def _machine(self) -> EnigmaMachine:
        return EnigmaMachine(
            rotors=tuple(var.get() for var in self.rotor_vars),
            positions="".join(var.get() for var in self.position_vars),
            ring_settings="".join(var.get() for var in self.ring_vars),
            reflector=self.reflector_var.get(),
            plugboard=self.plugboard_var.get(),
        )

    def process_message(self) -> None:
        message = self.input_text.get("1.0", "end-1c")
        try:
            machine = self._machine()
            result = machine.process(message)
        except ValueError as exc:
            messagebox.showerror("Invalid machine settings", str(exc), parent=self)
            return
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.output_text.configure(state="disabled")
        self._show_positions(machine.positions)
        final_letter = next((c for c in reversed(result) if c in ALPHABET), "")
        self._light(final_letter)
        self.status.configure(text=f"COMPLETE  /  {sum(c.upper() in ALPHABET and c.isascii() for c in message)} LETTERS STEPPED")

    def _show_positions(self, positions: str) -> None:
        self.position_display.configure(text=f"ROTOR WINDOWS     {'   '.join(positions)}")
        for var, letter in zip(self.position_vars, positions, strict=True):
            var.set(letter)

    def _light(self, letter: str) -> None:
        for key, lamp in self.lamp_labels.items():
            active = key == letter
            lamp.configure(bg=BRASS if active else "#353a32", fg="#171b18" if active else "#777665")

    def reset_windows(self) -> None:
        for var in self.position_vars:
            var.set("A")
        self._show_positions("AAA")
        self._light("")
        self.status.configure(text="WINDOWS RESET  /  READY")

    def clear_messages(self) -> None:
        self.input_text.delete("1.0", "end")
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
        self._light("")
        self.status.configure(text="READY")


def main() -> None:
    """Launch the desktop application."""
    EnigmaConsole().mainloop()


if __name__ == "__main__":
    main()
