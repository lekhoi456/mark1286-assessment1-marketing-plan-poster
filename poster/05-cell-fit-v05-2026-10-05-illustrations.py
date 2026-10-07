"""Simple flat-fill Section 5 journey pictures in native poster coordinates."""

NAVY = '#173a47'
CYAN = '#28bdbf'
GOLD = '#e3bb42'
CREAM = '#fdfbef'


def journey_art():
    """Return three bounded vector pictures; the caller supplies connectors."""
    return f'''
<g id="section-05-journey-pictures" stroke="{NAVY}" stroke-width="0.8" stroke-linecap="round" stroke-linejoin="round">
  <g id="section-05-landing-page-picture">
    <rect x="350.5" y="486.5" width="71" height="42" rx="2" fill="{CREAM}"/>
    <path d="M352.5 486.5H419.5Q421.5 486.5 421.5 488.5V493H350.5V488.5Q350.5 486.5 352.5 486.5Z" fill="{CYAN}"/>
    <path d="M356 503L365 495.5L374 503V514H356Z" fill="{GOLD}"/>
    <path d="M374 501L385.5 496L397 501V514H374Z" fill="{CYAN}"/>
    <path d="M397 503L407 495.5L417 503V514H397Z" fill="{GOLD}"/>
    <path d="M356 503H374 M374 501H397 M397 503H417" fill="none"/>
    <rect x="357" y="517.5" width="58" height="4" rx="1.5" fill="{CREAM}"/>
    <rect x="357" y="523.5" width="58" height="3.5" rx="1.5" fill="{CYAN}"/>
  </g>
  <g id="section-05-booking-phone-picture">
    <rect x="445.5" y="482.5" width="28" height="50" rx="3.5" fill="{CYAN}"/>
    <rect x="448.5" y="488" width="22" height="39" rx="1.5" fill="{CREAM}"/>
    <path d="M455.5 485.2H463.5" fill="none"/>
    <circle cx="453.5" cy="496" r="2.5" fill="{GOLD}"/>
    <path d="M456 496H459.5Q464.5 496 464.5 501V505" fill="none" stroke-width="1.2"/>
    <path d="M464.5 515C462.8 512.4 460.5 510.7 460.5 508.5A4 4 0 0 1 468.5 508.5C468.5 510.7 466.2 512.4 464.5 515Z" fill="{CYAN}"/>
    <circle cx="464.5" cy="508.5" r="1.1" fill="{CREAM}" stroke="none"/>
    <rect x="451" y="520" width="17" height="5" rx="1.5" fill="{GOLD}"/>
    <path d="M457 529.6H462" fill="none"/>
  </g>
  <g id="section-05-electric-taxi-picture">
    <path d="M528 493H543V497H528Z" fill="{GOLD}"/>
    <path d="M498 510L517 507L525 497H554L566 507L589 510Q596.5 511 597.5 515V522.5H497V514Q497 511 498 510Z" fill="{CYAN}"/>
    <path d="M520.5 506.5L527 499.5H540V506.5Z" fill="{CREAM}"/>
    <path d="M543 499.5H552.5L561 506.5H543Z" fill="{CREAM}"/>
    <circle cx="548" cy="502.5" r="2.5" fill="{GOLD}"/>
    <path d="M543.5 506.5Q548 503.5 552.5 506.5" fill="{CYAN}"/>
    <path d="M540.5 510V520 M564 509V520" fill="none"/>
    <path d="M549 510H554" fill="none"/>
    <path d="M533 512L528 517H533L530 521L539 515H534L538 512Z" fill="{GOLD}" stroke-width="0.65"/>
    <circle cx="516" cy="525" r="5.5" fill="{NAVY}"/>
    <circle cx="578" cy="525" r="5.5" fill="{NAVY}"/>
    <circle cx="516" cy="525" r="2.3" fill="{CREAM}" stroke="none"/>
    <circle cx="578" cy="525" r="2.3" fill="{CREAM}" stroke="none"/>
    <path d="M575.5 487.5H596Q599.5 487.5 599.5 491V502Q599.5 505.5 596 505.5H581L576 509V505.5H575.5Q572 505.5 572 502V491Q572 487.5 575.5 487.5Z" fill="{GOLD}"/>
    <circle cx="586" cy="495" r="2.7" fill="{CREAM}"/>
    <path d="M580.5 502V500.5Q586 496.5 591.5 500.5V502Z" fill="{CYAN}"/>
    <path d="M580.5 496V494Q580.5 490 586 490Q591.5 490 591.5 494V496" fill="none"/>
    <path d="M580.5 494.5V497 M591.5 494.5V497L588.5 498" fill="none" stroke-width="1.5"/>
  </g>
</g>'''
