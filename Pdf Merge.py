import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Button, END
from PyPDF2 import PdfMerger
from tkinterdnd2 import DND_FILES, TkinterDnD

class PDFMergerApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("📎 Drag & Drop PDF Merger")
        self.geometry("500x400")
        self.configure(bg="#f0f0f0")

        self.pdf_listbox = Listbox(self, selectmode=tk.SINGLE, width=60, height=15)
        self.pdf_listbox.pack(pady=20)

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop_files)

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack()

        Button(btn_frame, text="➕ Add Files", command=self.add_files).pack(side=tk.LEFT, padx=5)
        Button(btn_frame, text="🗑 Remove Selected", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        Button(btn_frame, text="📎 Merge PDFs", command=self.merge_pdfs).pack(side=tk.LEFT, padx=5)

    def drop_files(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            if file.endswith('.pdf') and file not in self.pdf_listbox.get(0, END):
                self.pdf_listbox.insert(END, file)

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for file in files:
            if file not in self.pdf_listbox.get(0, END):
                self.pdf_listbox.insert(END, file)

    def remove_selected(self):
        selected = self.pdf_listbox.curselection()
        if selected:
            self.pdf_listbox.delete(selected)

    def merge_pdfs(self):
        pdf_files = list(self.pdf_listbox.get(0, END))
        if len(pdf_files) < 2:
            messagebox.showwarning("Need more PDFs", "Please add at least two PDFs to merge.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if not output_path:
            return

        merger = PdfMerger()
        try:
            for pdf in pdf_files:
                merger.append(pdf)
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Success", f"Merged PDF saved at:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")

if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()


