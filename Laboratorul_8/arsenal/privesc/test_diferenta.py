def test_doar_ce_e_nou():
    # date scrise de mana: ce e in acum si nu e in baza
    acum = {"a", "b", "c"}
    baza = {"a", "b"}
    assert acum - baza == {"c"}
