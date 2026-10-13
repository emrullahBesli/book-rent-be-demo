#!/usr/bin/env python3
"""Proje tanıtım PDF'ini üretir (Pango + Cairo, harici paket yok)."""

from pathlib import Path

import cairo
import gi

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo  # noqa: E402

A4_W, A4_H = 595.28, 841.89
MM = 72 / 25.4
MARGIN_X = 18 * MM
MARGIN_TOP = 18 * MM
MARGIN_BOTTOM = 16 * MM
NAVY = (0.12, 0.20, 0.32)
ACCENT = (0.18, 0.42, 0.62)
TEXT = (0.15, 0.16, 0.18)
MUTED = (0.40, 0.42, 0.45)
RULE = (0.78, 0.80, 0.83)

OUT = Path(__file__).resolve().parent / "proje-tanitim.pdf"


def layout(ctx, markup, width, justify=False):
    lo = PangoCairo.create_layout(ctx)
    lo.set_width(int(width * Pango.SCALE))
    lo.set_wrap(Pango.WrapMode.WORD_CHAR)
    if justify:
        lo.set_justify(True)
    lo.set_markup(markup, -1)
    return lo


def paint_layout(ctx, lo, x, y, color=TEXT):
    ctx.save()
    ctx.set_source_rgb(*color)
    ctx.move_to(x, y)
    PangoCairo.update_layout(ctx, lo)
    PangoCairo.show_layout(ctx, lo)
    ctx.restore()
    _ink, logical = lo.get_extents()
    return logical.height / Pango.SCALE


def heading(ctx, text, width):
    return layout(
        ctx,
        f'<span font="Liberation Sans Bold 12" foreground="#1E3A5F">{text}</span>',
        width,
    )


def body(ctx, text, width):
    return layout(
        ctx,
        f'<span font="Liberation Serif 10.5" foreground="#26282C">{text}</span>',
        width,
        justify=True,
    )


def bullet(ctx, text, width):
    return layout(
        ctx,
        f'<span font="Liberation Serif 10.5" foreground="#26282C">•  {text}</span>',
        width,
    )


def small(ctx, text, width):
    return layout(
        ctx,
        f'<span font="Liberation Sans 8.5" foreground="#6A6E73">{text}</span>',
        width,
    )


def draw_header(ctx, page):
    ctx.set_source_rgb(*NAVY)
    ctx.rectangle(0, 0, A4_W, 22 * MM)
    ctx.fill()
    ctx.set_source_rgb(1, 1, 1)
    lo = layout(
        ctx,
        '<span font="Liberation Sans 9">BOOK RENT API  ·  PROJE TANITIM DOKÜMANI</span>',
        A4_W - 2 * MARGIN_X - 70,
    )
    ctx.move_to(MARGIN_X, 8.2 * MM)
    PangoCairo.show_layout(ctx, lo)

    right = layout(
        ctx,
        f'<span font="Liberation Sans 9">Sayfa {page} / 2</span>',
        50 * MM,
    )
    rw = right.get_extents()[1].width / Pango.SCALE
    ctx.move_to(A4_W - MARGIN_X - rw, 8.2 * MM)
    PangoCairo.show_layout(ctx, lo)

    ctx.set_source_rgb(*ACCENT)
    ctx.rectangle(0, 22 * MM, A4_W, 1.4)
    ctx.fill()


def draw_footer(ctx):
    y = A4_H - 11 * MM
    ctx.set_source_rgb(*RULE)
    ctx.set_line_width(0.6)
    ctx.move_to(MARGIN_X, y)
    ctx.line_to(A4_W - MARGIN_X, y)
    ctx.stroke()
    lo = layout(
        ctx,
        '<span font="Liberation Sans 8">Emrullah Besli  ·  In-memory REST API  ·  Node.js / Express</span>',
        A4_W - 2 * MARGIN_X,
    )
    ctx.set_source_rgb(*MUTED)
    ctx.move_to(MARGIN_X, y + 3)
    PangoCairo.show_layout(ctx, lo)


def main():
    surface = cairo.PDFSurface(str(OUT), A4_W, A4_H)
    ctx = cairo.Context(surface)
    width = A4_W - 2 * MARGIN_X
    page = 1
    y = 26 * MM

    def new_page():
        nonlocal page, y
        draw_footer(ctx)
        ctx.show_page()
        page += 1
        draw_header(ctx, page)
        y = 28 * MM

    def ensure(h):
        nonlocal y
        if y + h > A4_H - MARGIN_BOTTOM:
            new_page()

    def add(lo, gap=6, color=TEXT):
        nonlocal y
        h = lo.get_extents()[1].height / Pango.SCALE
        ensure(h + gap)
        paint_layout(ctx, lo, MARGIN_X, y, color)
        y += h + gap

    draw_header(ctx, page)

    add(
        layout(
            ctx,
            '<span font="Liberation Sans Bold 20" foreground="#1E3A5F">Book Rent API</span>',
            width,
        ),
        gap=4,
    )
    add(
        layout(
            ctx,
            '<span font="Liberation Sans 11" foreground="#2E6A9E">Kısa amaç, senaryo ve sistem özeti</span>',
            width,
        ),
        gap=8,
    )
    add(
        small(
            ctx,
            "Hazırlayan: Emrullah Besli    |    Tarih: Eylül 2026    |    Sürüm: 1.0    |    Taban URL: http://localhost:3000/api/v1",
            width,
        ),
        gap=10,
    )

    ctx.set_source_rgb(*RULE)
    ctx.set_line_width(0.8)
    ctx.move_to(MARGIN_X, y)
    ctx.line_to(A4_W - MARGIN_X, y)
    ctx.stroke()
    y += 12

    add(heading(ctx, "1. Amaç", width), gap=6)
    add(
        body(
            ctx,
            "Book Rent API, küçük ölçekli bir kitap kiralama işini REST arayüzü üzerinden sunmak için geliştirilmiş "
            "bir arka uç uygulamasıdır. Hedef; karmaşık bir altyapı kurmadan, katmanlı ve okunabilir bir Express.js "
            "servisi ile kimlik doğrulama, kitap envanteri ve kiralama döngüsünü uçtan uca göstermektir. Kalıcı "
            "veritabanı yoktur: kullanıcılar, kitaplar ve kiralamalar uygulama belleğinde tutulur. Sunucu yeniden "
            "başlatıldığında veriler başlangıç (seed) haline döner. Proje eğitim / ödev kapsamında demo niteliğindedir; "
            "üretim ortamı, ödeme veya kullanıcı kaydı bu sürümün dışında bırakılmıştır.",
            width,
        ),
        gap=14,
    )

    add(heading(ctx, "2. Senaryo", width), gap=6)
    add(
        body(
            ctx,
            "Tipik akış bir kütüphane veya kiralama gişesinin dijital karşılığıdır. Kullanıcı sisteme giriş yapar, "
            "müsait kitapları inceler, stoğu olan bir kitabı kiralar ve süresi dolduğunda iade eder. Yönetim tarafında "
            "ise katalog güncellenebilir.",
            width,
        ),
        gap=8,
    )

    steps = [
        "<b>Giriş.</b> Kullanıcı adı ve şifre ile oturum açılır. Yanıtta HS256 JWT döner; login dışındaki tüm istekler "
        "<tt>Authorization: Bearer</tt> ister.",
        "<b>Katalog.</b> Kitaplar sayfalı listelenir (<tt>page</tt>, <tt>limit</tt>) veya kimlik ile tek kayıt getirilir. "
        "Her kitapta ad, fiyat ve stok bulunur.",
        "<b>Kiralama.</b> Stok en az 1 ise kiralama kaydı oluşur ve stok bir azalır. Stok yoksa işlem 409 ile reddedilir "
        "(örnek seed: <i>Sefiller</i>).",
        "<b>İade.</b> Yalnızca kiralayan kullanıcı iade edebilir; stok bir artar. Tekrar iade 409, başkasının kaydı 403 döner.",
        "<b>Yönetim.</b> Yetkili oturumla kitap ekleme, güncelleme ve silme yapılabilir.",
        "<b>Çıkış.</b> Logout token’ı bellek içi oturum listesinden siler; aynı JWT ile sonraki istekler 401 alır.",
    ]
    for s in steps:
        add(
            layout(
                ctx,
                f'<span font="Liberation Serif 10.5" foreground="#26282C">•  {s}</span>',
                width,
            ),
            gap=5,
        )

    y += 6
    add(heading(ctx, "3. Sistem özeti", width), gap=6)
    add(
        body(
            ctx,
            "Uygulama Node.js üzerinde Express ile çalışır. Kaynak kod <tt>src/</tt> altında katmanlara ayrılmıştır: "
            "rotalar HTTP yollarını, denetleyiciler istek/yanıtı, servisler iş kurallarını, modeller seed veriyi tutar. "
            "Kesit kaygısı taşıyan işler ara yazılımlardadır.",
            width,
        ),
        gap=8,
    )

    layers = [
        "<b>Güvenlik ve günlük.</b> Helmet, CORS, JSON gövde sınırı (10 KB), istek kimliği (<tt>x-request-id</tt>) ve Morgan HTTP logu. "
        "Tanımsız rota 404; merkezi hata yakalayıcı JSON (<tt>success: false</tt>, <tt>message</tt>, <tt>requestId</tt>) üretir.",
        "<b>Kimlik.</b> JWT (<tt>JWT_SECRET</tt>, varsayılan süre 8 saat) imzalanır ve logout için bellek içi oturum haritasında da tutulur. "
        "Demo kullanıcılar: <tt>admin / admin123</tt>, <tt>emrullah / 123456</tt>.",
        "<b>Veri.</b> Kullanıcı (<tt>id, username, password</tt>), kitap (<tt>id, name, price, stock</tt>), kiralama "
        "(<tt>id, bookId, userId, rentedAt, returnedAt</tt>). Kiralama kimliği UUID’dir.",
        "<b>Çalıştırma.</b> <tt>npm install</tt>, kökte <tt>.env</tt> (<tt>PORT</tt>, <tt>NODE_ENV</tt>, <tt>JWT_SECRET</tt>), ardından <tt>npm start</tt>.",
    ]
    for s in layers:
        add(
            layout(
                ctx,
                f'<span font="Liberation Serif 10.5" foreground="#26282C">•  {s}</span>',
                width,
            ),
            gap=5,
        )

    y += 8
    add(heading(ctx, "4. Uç nokta özeti", width), gap=8)

    rows = [
        ("POST", "/auth/login", "Oturum aç; JWT üretir (public)"),
        ("POST", "/auth/logout", "Token’ı geçersiz kılar"),
        ("GET", "/books", "Sayfalı liste (page, limit; max 50)"),
        ("GET", "/books/:id", "Tek kitap"),
        ("POST", "/books", "Kitap ekle (name, price, stock)"),
        ("PUT", "/books/:id", "Kısmi güncelleme"),
        ("DELETE", "/books/:id", "Kitap sil"),
        ("POST", "/rentals", "Kirala { bookId } — stok düşer"),
        ("POST", "/rentals/:id/return", "İade — stok artar"),
    ]

    col_m, col_p, col_d = 52, 150, width - 52 - 150
    header_h = 16
    row_h = 15
    table_h = header_h + len(rows) * row_h + 4
    ensure(table_h + 24)

    ctx.set_source_rgb(*NAVY)
    ctx.rectangle(MARGIN_X, y, width, header_h)
    ctx.fill()
    ctx.set_source_rgb(1, 1, 1)
    for label, xoff in (("Metot", 6), ("Yol", col_m + 6), ("Açıklama", col_m + col_p + 6)):
        lo = layout(ctx, f'<span font="Liberation Sans Bold 8">{label}</span>', 200)
        ctx.move_to(MARGIN_X + xoff, y + 3)
        PangoCairo.show_layout(ctx, lo)
    y += header_h

    for i, (method, path, desc) in enumerate(rows):
        if i % 2 == 0:
            ctx.set_source_rgb(0.94, 0.96, 0.98)
            ctx.rectangle(MARGIN_X, y, width, row_h)
            ctx.fill()
        ctx.set_source_rgb(*TEXT)
        cells = [
            (f'<span font="Liberation Sans Bold 8" foreground="#2E6A9E">{method}</span>', 6, col_m - 8),
            (f'<span font="Liberation Sans 8"><tt>{path}</tt></span>', col_m + 6, col_p - 8),
            (f'<span font="Liberation Serif 8.5">{desc}</span>', col_m + col_p + 6, col_d - 10),
        ]
        for markup, xoff, w in cells:
            lo = layout(ctx, markup, w)
            ctx.move_to(MARGIN_X + xoff, y + 2.2)
            PangoCairo.show_layout(ctx, lo)
        y += row_h

    ctx.set_source_rgb(*RULE)
    ctx.set_line_width(0.5)
    ctx.rectangle(MARGIN_X, y - len(rows) * row_h - header_h, width, header_h + len(rows) * row_h)
    ctx.stroke()
    y += 12

    add(
        small(
            ctx,
            "Tüm yollar /api/v1 öneki ile çağrılır. Login hariç Bearer JWT zorunludur. Ayrıntılı örnekler: docs/api.md, "
            "entegrasyon: docs/kullanim.md, senaryo testleri: docs/test.md.",
            width,
        ),
        gap=12,
    )

    add(heading(ctx, "5. Kapsam ve sınırlar", width), gap=6)
    add(
        body(
            ctx,
            "Bu sürüm tek süreçli bellek modeli kullanır; ölçekleme, çoklu sunucu oturumu ve kalıcı depolama yoktur. "
            "Şifreler düz metin seed’dedir (demo). JWT imza anahtarı ortam dosyasındandır ve git’e eklenmez. "
            "Sistem, kiralama stoğu ve oturum yaşam döngüsünü sade bir API olarak belgelemek ve denemek için yeterlidir.",
            width,
        ),
        gap=8,
    )

    draw_footer(ctx)
    surface.finish()
    print(f"Yazıldı: {OUT}")


if __name__ == "__main__":
    main()
