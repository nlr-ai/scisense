import React from 'react';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer>
      <div className="container">
        <div className="footer-grid">
          <div className="footer-column">
            <h3>SciSense</h3>
            <p>Expertise en Affaires Scientifiques &amp; Médicales spécialisée dans les stratégies médico-scientifiques internationales et l'IA pour la recherche.</p>
            <div className="social-links">
              <a href="https://www.linkedin.com/in/aurore-inchausp%C3%A9-2493938b/" target="_blank" rel="noopener noreferrer" className="social-link" aria-label="LinkedIn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                </svg>
              </a>
              <a href="mailto:aurore.inchauspe@scisence.fr" className="social-link" aria-label="Email">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M0 3v18h24v-18h-24zm21.518 2l-9.518 7.713-9.518-7.713h19.036zm-19.518 14v-11.817l10 8.104 10-8.104v11.817h-20z"/>
                </svg>
              </a>
              <a href="tel:+33629894916" className="social-link" aria-label="Phone">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20 22.621l-3.521-6.795c-.008.004-1.974.97-2.064 1.011-2.24 1.086-6.799-7.82-4.609-8.994l2.083-1.026-3.493-6.817-2.106 1.039c-7.202 3.755 4.233 25.982 11.6 22.615.121-.055 2.102-1.029 2.11-1.033z"/>
                </svg>
              </a>
            </div>
          </div>
          <div className="footer-column">
            <h3>Navigation</h3>
            <ul className="footer-links">
              <li><Link href="/">Accueil</Link></li>
              <li><Link href="/about">À propos</Link></li>
              <li><Link href="/services">Services</Link></li>
              <li><Link href="/case-studies">Projets</Link></li>
              <li><Link href="/blog">Blog</Link></li>
              <li><Link href="/contact">Contact</Link></li>
            </ul>
          </div>
          <div className="footer-column">
            <h3>Services</h3>
            <ul className="footer-links">
              <li><Link href="/services#strategy">Stratégie Médicale Internationale</Link></li>
              <li><Link href="/services#kol">Gestion de Réseaux KOL</Link></li>
              <li><Link href="/services#ai">IA pour la Recherche</Link></li>
              <li><Link href="/services#communication">Communication Scientifique</Link></li>
              <li><Link href="/services#training">Formation Médicale</Link></li>
            </ul>
          </div>
          <div className="footer-column">
            <h3>Contact</h3>
            <p>Pour toute demande de collaboration ou d'information, n'hésitez pas à nous contacter.</p>
            <p><strong>Email:</strong> <a href="mailto:aurore.inchauspe@scisence.fr">aurore.inchauspe@scisence.fr</a><br />
            <strong>Tél:</strong> <a href="tel:+33629894916">06.29.89.49.16</a></p>
            <Link href="/contact" className="button">Prendre rendez-vous</Link>
          </div>
        </div>
        <div className="copyright">
          &copy; {new Date().getFullYear()} SciSense. Tous droits réservés.
        </div>
      </div>
    </footer>
  );
}
