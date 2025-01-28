import base64
import re
from typing import Optional

from django.conf import settings

from decouple_nacl import (
  avaaja,
  Csv,
  julkinen_avain,
  salaaja,
  yksityinen_avain,
  JULKINEN_AVAIN,
  SALATTU,
  YKSITYINEN_AVAIN,
)
from nacl.public import PrivateKey, PublicKey, SealedBox


def salaa_data(julkinen_avain: Optional[str] = None):
  ''' Salaa vakiosyötteestä luettu data annetulla julkisella avaimella. '''
  import sys
  julkinen_avain = julkinen_avain or settings.CONFIG(JULKINEN_AVAIN)
  salaaja = SealedBox(PublicKey(base64.b64decode(julkinen_avain)))
  muunnos = re.compile(r'([^=]+=)(.*)')
  for data in sys.stdin:
    if parametri := muunnos.match(data):
      salattu = base64.b64encode(
        salaaja.encrypt(parametri.group(2).encode())
      ).decode()
      print(f'{parametri.group(1)}!{{{salattu}}}')
    else:
      print(data)
  # def salaa_data


def luo_avainpari(tulosta: bool = True) -> tuple[PrivateKey, PublicKey]:
  ''' Luo ja tulosta uusi NaCl-avainpari. '''
  sk = PrivateKey.generate()
  pk = sk.public_key
  if tulosta:
    print('Tallenna tämä suojattuun .env-tiedostoon palvelimella:')
    print(f'{YKSITYINEN_AVAIN}={base64.b64encode(sk.encode()).decode()}')
    print()
    print('Vie tämä versiohallittuun, julkisesti jaettuun .env-tiedostoon:')
    print(f'{JULKINEN_AVAIN}={base64.b64encode(pk.encode()).decode()}')
  return sk, pk
  # def luo_avainpari


def vaihda_avainta():
  ''' Luo uusi avainpari. Tulosta tarvittavat muutokset .env-tiedostoihin. '''
  vanha_julkinen_avain = julkinen_avain(settings.CONFIG)
  vanha_yksityinen_avain = yksityinen_avain(settings.CONFIG)
  vanha_avaaja = avaaja(settings.CONFIG)

  uusi_yksityinen_avain, uusi_julkinen_avain = luo_avainpari(False)
  uusi_salaaja = SealedBox(uusi_julkinen_avain)

  # Tulostetaan diff yksityisten avaimien vaihtoon.
  vanhat_yksityiset_avaimet: str = settings.CONFIG(YKSITYINEN_AVAIN)
  uudet_yksityiset_avaimet: str = ', '.join((
    base64.b64encode(vanha_yksityinen_avain.encode()).decode(),  # vanha
    base64.b64encode(uusi_yksityinen_avain.encode()).decode(),  # uusi
  ))
  print(' ### YKSITYINEN AVAIN, SÄILYTÄ SUOJATTUNA!')
  print()
  print(f'-{YKSITYINEN_AVAIN}={vanhat_yksityiset_avaimet}')
  print(f'+{YKSITYINEN_AVAIN}={uudet_yksityiset_avaimet}')
  print()
  print()

  # Käydään läpi kaikki (salatut ja salaamattomat) asetusparametrit.
  # Tällöin `decouple_nacl` muodostaa sanakirjan
  # `settings.CONFIG._salatut_parametrit`.
  for avain in settings.CONFIG:
    settings.CONFIG(avain)

  # Tulostetaan diff julkisen avaimen vaihtoon.
  vanha_julkinen_avain_b64 = base64.b64encode(
    vanha_julkinen_avain.encode()
  ).decode()
  uusi_julkinen_avain_b64 = base64.b64encode(
    uusi_julkinen_avain.encode()
  ).decode()
  print(' ### JULKISET PARAMETRIT')
  print()
  print(f'-{JULKINEN_AVAIN}={vanha_julkinen_avain_b64}')
  print(f'+{JULKINEN_AVAIN}={uusi_julkinen_avain_b64}')
  print()

  # Tulostetaan diff kaikkien salattujen arvojen vaihtoon.
  for avain, vanha_arvo in settings.CONFIG._salatut_parametrit.items():
    def vaihda_avain(salattu: re.Match) -> str:
      salattu = base64.b64decode(salattu.group(1))
      purettu = vanha_avaaja.decrypt(salattu)
      return f'!{{{base64.b64encode(uusi_salaaja.encrypt(purettu)).decode()}}}'
    uusi_arvo = SALATTU.sub(vaihda_avain, vanha_arvo)
    print(f'-{avain}={vanha_arvo}')
    print(f'+{avain}={uusi_arvo}')
    # for avain, vanha_arvo in settings.CONFIG._salatut_parametrit.items

  # def vaihda_avainta
