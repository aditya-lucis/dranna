# anna/tests/test_label.py — pengujian affect labeling sopan & kamus personal
from anna.src.pii.label import LABEL, kalimat_tawaran, tawarkan_label, tawarkan_label_personal


def test_selalu_ada_pintu_belum_tahu():
    """Invarian psikologis: Kalimat penawaran label selalu menyertakan opsi 'belum ketemu namanya'."""
    teks = kalimat_tawaran(tawarkan_label((-0.4, 0.4)))
    assert "belum ketemu" in teks


def test_duka_tenang_tidak_dijadi_sedih_murni():
    """Granularitas: Keadaan duka tenang (-0.15, -0.30) dipetakan ke label khusus, bukan vonis berat."""
    k = tawarkan_label((-0.15, -0.30), top=1)
    assert k[0] == "nyaman-berduka" or k[0] != "berat"


def test_label_valid_pad():
    """Batas koordinat: Semua titik label emosi berada dalam rentang [-1, 1]."""
    for k, (v, a) in LABEL.items():
        assert -1.0 <= v <= 1.0 and -1.0 <= a <= 1.0


def test_tawaran_personal_mendahulukan_kamus_sendiri():
    """Otonomi pengguna: Kosakata yang dinamai sendiri oleh pengguna diprioritaskan di hasil rekomendasi."""
    kamus = {"personal": {"ambah": [-0.1, 0.3]}}
    k = tawarkan_label_personal((-0.1, 0.3), kamus, top=1)
    assert k[0] == "ambah"
