import React from 'react';
import Link from 'next/link';

export default function NotFound() {
  return (
    <main>
      <section className="section">
        <div className="container text-center">
          <h1>Page non trouvée</h1>
          <p>Désolé, la page que vous recherchez n'existe pas ou a été déplacée.</p>
          <Link href="/" className="button">Retourner à l'accueil</Link>
        </div>
      </section>
    </main>
  );
}
