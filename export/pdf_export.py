from reportlab.pdfgen import canvas

def export_pdf(images):

    c = canvas.Canvas("lecture_notes.pdf")

    y=700

    for img in images:

        c.drawImage(img,50,y,width=500,height=300)

        y-=320

        if y<100:

            c.showPage()
            y=700

    c.save()