"""
Lista completa de ações negociadas na B3
Fonte: Principais ações por liquidez e volume
"""

def get_acoes_b3_completas():
    """Retorna lista expandida com 200+ ações da B3."""
    
    acoes = [
        # === FINANCEIRO (Bancos, Seguros, Serviços Financeiros) ===
        "ITUB3.SA", "ITUB4.SA", "BBDC3.SA", "BBDC4.SA", "BBAS3.SA", 
        "SANB11.SA", "BPAC11.SA", "BRSR6.SA", "PINE4.SA", "BMGB4.SA",
        "BBSE3.SA", "PSSA3.SA", "SULA11.SA", "WIZS3.SA", "BPAN4.SA",
        "CIEL3.SA", "CIELO3.SA", "PAGSEGURO31.SA", "STBP3.SA",
        
        # === PETRÓLEO, GÁS E COMBUSTÍVEIS ===
        "PETR3.SA", "PETR4.SA", "PRIO3.SA", "RECV3.SA", "RRRP3.SA",
        "PEAB3.SA", "PEAB4.SA", "UGPA3.SA", "CSAN3.SA", "RAIZ4.SA",
        "ENEV3.SA", "ENAT3.SA",
        
        # === MINERAÇÃO E SIDERURGIA ===
        "VALE3.SA", "BRAP3.SA", "BRAP4.SA", "GOAU4.SA", "CMIN3.SA", 
        "GGBR3.SA", "GGBR4.SA", "USIM3.SA", "USIM5.SA", "CSNA3.SA",
        "GERDAUGMET3.SA", "FESA3.SA", "FESA4.SA",
        
        # === ENERGIA ELÉTRICA ===
        "ELET3.SA", "ELET6.SA", "TAEE11.SA", "TAEE3.SA", "TAEE4.SA",
        "EGIE3.SA", "CPLE3.SA", "CPLE5.SA", "CPLE6.SA", "CMIG3.SA", 
        "CMIG4.SA", "ENBR3.SA", "NEOE3.SA", "CESP6.SA", "CPFE3.SA",
        "TIET3.SA", "TIET4.SA", "TRPL3.SA", "TRPL4.SA", "LIGT3.SA",
        "ALUP11.SA", "ALUP3.SA", "ALUP4.SA", "COCE3.SA", "COCE5.SA",
        "ENGI11.SA", "ENGI3.SA", "ENGI4.SA", "EQTL3.SA", "MEGA3.SA",
        "RNEW11.SA", "RNEW3.SA", "RNEW4.SA", "AESB3.SA", "AURE3.SA",
        
        # === SANEAMENTO ===
        "SAPR11.SA", "SAPR3.SA", "SAPR4.SA", "SBSP3.SA", "CSMG3.SA",
        "CGNA3.SA", "SANEPAR.SA",
        
        # === TELECOMUNICAÇÕES ===
        "TIMS3.SA", "VIVT3.SA", "OIBR3.SA", "OIBR4.SA", "TELB4.SA",
        
        # === CONSUMO (Alimentos e Bebidas) ===
        "ABEV3.SA", "JBSS3.SA", "BEEF3.SA", "MRFG3.SA", "SMTO3.SA",
        "NTCO3.SA", "CAML3.SA", "MDIA3.SA", "SLCE3.SA", "LAND3.SA",
        "M3LK3.SA", "JALL3.SA", "BLAU3.SA",
        
        # === VAREJO ===
        "LREN3.SA", "MGLU3.SA", "VVAR3.SA", "PETZ3.SA", "SOMA3.SA", 
        "GUAR3.SA", "VIIA3.SA", "CEAB3.SA", "VULC3.SA", "GRND3.SA",
        "AMER3.SA", "ARZZ3.SA", "CRFB3.SA", "IGTI11.SA", "IGTI3.SA",
        "AMAR3.SA", "ALPK3.SA", "ATOM3.SA", "FTCE3.SA", "LEVE3.SA",
        "PCAR3.SA", "LAME3.SA", "LAME4.SA", "RAPT4.SA", "TFCO4.SA",
        
        # === INDÚSTRIA (Diversos) ===
        "WEGE3.SA", "EMBR3.SA", "EMAE4.SA", "MYPK3.SA", "TUPY3.SA",
        "ROMI3.SA", "KEPL3.SA", "FRAS3.SA", "RAPT3.SA", "VLID3.SA",
        "WHRL4.SA", "RANI3.SA", "POMO3.SA", "POMO4.SA", "TECN3.SA",
        
        # === PAPEL E CELULOSE ===
        "KLBN11.SA", "KLBN3.SA", "KLBN4.SA", "SUZB3.SA", "SUZB5.SA",
        "FIBR3.SA", "MELK3.SA",
        
        # === CONSTRUÇÃO CIVIL E IMOBILIÁRIO ===
        "CYRE3.SA", "MRVE3.SA", "EZTC3.SA", "TEND3.SA", "JHSF3.SA",
        "EVEN3.SA", "HBOR3.SA", "DIRR3.SA", "LAVV3.SA", "PLPL3.SA",
        "CALI3.SA", "CALI4.SA", "OPCT3.SA", "MTRE3.SA", "TCSA3.SA",
        "RSID3.SA", "MDNE3.SA", "GFSA3.SA",
        
        # === SAÚDE ===
        "RDOR3.SA", "FLRY3.SA", "HAPV3.SA", "QUAL3.SA", "DASA3.SA",
        "GNDI3.SA", "PNVL3.SA", "CURY3.SA", "MATD3.SA", "ONCO3.SA",
        "ALLHEALTHCARE3.SA", "AALR3.SA", "HYPE3.SA",
        
        # === EDUCAÇÃO ===
        "COGN3.SA", "YDUQ3.SA", "ANIM3.SA", "SEER3.SA", "BAHI3.SA",
        
        # === LOGÍSTICA E TRANSPORTE ===
        "CCRO3.SA", "ECOR3.SA", "RADL3.SA", "RAIL3.SA", "AZUL4.SA",
        "GOLL4.SA", "EMBR3.SA", "LOGN3.SA", "JSL3.SA", "TGAR3.SA",
        "SIMH3.SA", "STTR3.SA",
        
        # === HOLDINGS E PARTICIPAÇÕES ===
        "ITSA3.SA", "ITSA4.SA", "MULT3.SA", "B3SA3.SA", "LWSA3.SA",
        "POSI3.SA", "TOTS3.SA", "RENT3.SA", "ALSO3.SA", "ALPA3.SA",
        "ALPA4.SA", "CVCB3.SA", "IRBR3.SA", "PDGR3.SA", "UNIP3.SA",
        "UNIP5.SA", "UNIP6.SA", "BIDI11.SA", "BIDI3.SA", "BIDI4.SA",
        
        # === TECNOLOGIA E TELECOM ===
        "LWSA3.SA", "POSI3.SA", "TOTS3.SA", "MOVI3.SA", "DESK3.SA",
        "SEQL3.SA", "INTB3.SA", "SQIA3.SA", "TRAD3.SA", "PGMN3.SA",
        
        # === AGRONEGÓCIO ===
        "SLCE3.SA", "LAND3.SA", "JALL3.SA", "CAML3.SA", "SOJA3.SA",
        "AGRO3.SA", "TTEN3.SA", "AGXY3.SA",
        
        # === QUÍMICO E PETROQUÍMICO ===
        "BRKM3.SA", "BRKM5.SA", "UNIP3.SA", "UNIP5.SA", "UNIP6.SA",
        "CTNM3.SA", "CTNM4.SA", "ELPL3.SA", "ELPL4.SA",
        
        # === OUTROS SETORES ===
        "AZEV4.SA", "BEES3.SA", "CEEB3.SA", "ENJU3.SA", "FIQE3.SA",
        "GOGL34.SA", "HETA4.SA", "LIPR3.SA", "NGRD3.SA", "OSXB3.SA",
        "PFRM3.SA", "PMAM3.SA", "RBVA11.SA", "RCSL3.SA", "RCSL4.SA",
        "SHUL4.SA", "SMFT3.SA", "SNSY5.SA", "VITT3.SA", "WIZC3.SA",
    ]
    
    return list(set(acoes))  # Remove duplicatas

def get_fiis_completos():
    """Retorna lista expandida com 100+ FIIs."""
    
    fiis = [
        # Lajes Corporativas
        "HGLG11.SA", "BTLG11.SA", "XPLG11.SA", "KNCR11.SA", "GGRC11.SA",
        "WTSP11B.SA", "EDGA11B.SA", "RBED11.SA", "FIGS11.SA", "ALMI11.SA",
        
        # Shoppings
        "XPML11.SA", "VISC11.SA", "HSML11.SA", "HSLG11.SA", "ABCP11.SA",
        "BRCO11.SA", "JRDM11.SA", "FVPQ11.SA", "NEWU11.SA", "ONEF11.SA",
        
        # Logística
        "HGRU11.SA", "HGRE11.SA", "VILG11.SA", "TRXF11.SA", "TGAR11.SA",
        "LVBI11.SA", "HGLG11.SA", "GBIO11.SA", "SPTW11.SA", "SDIL11.SA",
        
        # Híbridos
        "MXRF11.SA", "KNRI11.SA", "HGPO11.SA", "KNHY11.SA", "KNIP11.SA",
        "VGIR11.SA", "XPPR11.SA", "RCRB11.SA", "RECR11.SA", "RBRD11.SA",
        
        # Recebíveis
        "RZTR11.SA", "BCFF11.SA", "RBRR11.SA", "RBRF11.SA", "KFOF11.SA",
        "RBRX11.SA", "VRTA11.SA", "ALZR11.SA", "MCCI11.SA", "GGRC11.SA",
        
        # Títulos e Renda Fixa
        "PVBI11.SA", "IRDM11.SA", "BCRI11.SA", "RECT11.SA", "HGCR11.SA",
        "CPTS11.SA", "BTCI11.SA", "VSLH11.SA", "HTMX11.SA", "KNCA11.SA",
        
        # Residencial
        "HABT11.SA", "VINO11.SA", "RBVA11.SA", "VCJR11.SA", "RBRY11.SA",
        "HGBS11.SA", "NSLU11.SA", "HCTR11.SA", "DOMC11.SA", "PATL11.SA",
        
        # Agronegócio
        "AGCX11.SA", "SOJA11.SA", "LFTT11.SA", "TSNC11.SA",
        
        # Outros
        "JSRE11.SA", "MCHY11.SA", "DEVA11.SA", "BRCR11.SA", "XPCI11.SA",
        "GAME11.SA", "BTAL11.SA", "GALG11.SA", "GARE11.SA", "TRBL11.SA",
        "PORD11.SA", "PLRI11.SA", "BPFF11.SA", "SARE11.SA", "RURA11.SA",
        "KNSC11.SA", "VGIP11.SA", "XPHT11.SA", "RBRP11.SA", "RBRS11.SA",
    ]
    
    return list(set(fiis))
