import React from 'react';
import Link from 'next/link';
import MobileMenu from './MobileMenu';

export default function Header() {
  return (
    <header>
      <div className="container header-container">
        <div className="logo">
          <Link href="/" className="logo-link">
            <span className="logo-text">SciSense</span>
            <span className="logo-tagline">Making Science make sense</span>
          </Link>
        </div>
        <nav className="desktop-nav">
          <ul>
            {/* Removed "Accueil" */}
            <li><Link href="/about">À propos</Link></li>
            <li><Link href="/services">Services</Link></li>
            {/* Deactivated "Projets" and "Blog" by making them non-clickable spans */}
            <li><span className="disabled-link">Projets</span></li>
            <li><span className="disabled-link">Blog</span></li>
            <li className="cta-link"><Link href="/contact" className="button button-small">Contact</Link></li>
          </ul>
        </nav>
        <MobileMenu />
      </div>
    </header>
  );
}
