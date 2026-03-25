import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

export default function Home() {
  return (
    <main>
      <section className="hero">
        <div className="container">
          <h1>SciSense</h1>
          <h2>Making Science make sense</h2>
          <p className="hero-tagline">Expertise scientifique au service de vos projets médicaux</p>
          <div>
            <Link href="/contact" className="button">Prendre rendez-vous</Link>
            <Link href="/about" className="button button-secondary">En savoir plus</Link>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="section-title">
            <h2>Expertise</h2>
          </div>
          <p className="text-center">Spécialiste de la communication scientifique et des stratégies médico-marketing, je transforme la complexité scientifique en avantage stratégique pour votre organisation.</p>
          
          <div className="services">
            <div className="service-card">
              <h3>Stratégie Médicale Internationale</h3>
              <p>Développement et implémentation de stratégies médico-scientifiques dans plus de 10 pays, adaptées aux spécificités réglementaires et culturelles locales.</p>
            </div>
            <div className="service-card">
              <h3>Gestion de Réseaux KOL</h3>
              <p>Création et animation de réseaux d'experts médicaux pour faciliter l'échange de données cliniques et renforcer votre positionnement scientifique.</p>
            </div>
            <div className="service-card">
              <h3>IA pour la Recherche Scientifique</h3>
              <p>Implémentation de systèmes multi-agents pour l'analyse scientifique et la rédaction, optimisant vos processus de recherche et communication.</p>
            </div>
            <div className="service-card">
              <h3>Communication Scientifique</h3>
              <p>Rédaction et validation de publications, articles scientifiques et supports marketing conformes aux exigences réglementaires internationales.</p>
            </div>
          </div>
          
          <div className="text-center" style={{ marginTop: '2rem' }}>
            <Link href="/services" className="button">Découvrir tous mes services</Link>
          </div>
        </div>
      </section>
      
      <div className="divider"></div>
      
      <section className="section">
        <div className="container">
          <div className="section-title">
            <h2>Parcours d'Excellence</h2>
          </div>
          <div className="about-grid">
            <div className="about-content">
              <p>Du laboratoire à la stratégie internationale, notre approche unique combine rigueur scientifique et vision stratégique.</p>
              <ul>
                <li><strong>Expertise doctorale en Biologie Moléculaire</strong></li>
                <li><strong>Plus de 5 ans d'expérience</strong> en affaires scientifiques et médicales</li>
                <li><strong>Déploiement de stratégies dans 10 pays</strong> avec coordination d'équipes internationales</li>
                <li><strong>Développement de systèmes IA</strong> pour l'analyse et la rédaction scientifique</li>
              </ul>
              <Link href="/about" className="button">En savoir plus sur notre approche</Link>
            </div>
            <div className="about-image">
              {/* Placeholder for profile image */}
              <div style={{ backgroundColor: 'var(--light-blue)', height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary-violet)', fontWeight: 'bold' }}>
                Photo d'Aurore Inchauspé
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section className="testimonials">
        <div className="container">
          <div className="section-title">
            <h2>Témoignages</h2>
          </div>
          <div className="testimonial-container">
            <div className="testimonial">
              <p className="testimonial-text">"Aurore a transformé notre approche de la communication scientifique. Sa capacité à traduire des données complexes en messages stratégiques a considérablement renforcé notre positionnement auprès des professionnels de santé."</p>
              <p className="testimonial-author">— Directeur Marketing, Entreprise Pharmaceutique</p>
            </div>
            <div className="testimonial">
              <p className="testimonial-text">"L'expertise d'Aurore dans la gestion de réseaux KOL internationaux nous a permis d'établir des collaborations scientifiques précieuses dans plusieurs pays européens. Son approche rigoureuse et stratégique a été déterminante."</p>
              <p className="testimonial-author">— Responsable Affaires Médicales, Laboratoire International</p>
            </div>
          </div>
        </div>
      </section>
      
      <section className="section">
        <div className="container">
          <div className="section-title">
            <h2>Projets Récents</h2>
          </div>
          <div className="projects">
            <div className="project-card">
              <div className="project-image" style={{ backgroundColor: 'var(--light-violet)' }}></div>
              <div className="project-content">
                <h3>Système Multi-agents pour la Recherche Scientifique</h3>
                <p>Développement d'un système IA capable de rédiger des documents scientifiques et d'effectuer une lecture critique d'articles, optimisant les processus de recherche.</p>
                <Link href="/case-studies#ai-research">En savoir plus →</Link>
              </div>
            </div>
            <div className="project-card">
              <div className="project-image" style={{ backgroundColor: 'var(--light-blue)' }}></div>
              <div className="project-content">
                <h3>Stratégie Médico-Scientifique Multi-Pays</h3>
                <p>Élaboration et déploiement d'une stratégie cohérente adaptée aux spécificités de 10 marchés internationaux, incluant formation des équipes locales et développement d'outils de communication.</p>
                <Link href="/case-studies#international-strategy">En savoir plus →</Link>
              </div>
            </div>
          </div>
          <div className="text-center" style={{ marginTop: '2rem' }}>
            <Link href="/case-studies" className="button">Voir tous les projets</Link>
          </div>
        </div>
      </section>
      
      <div className="divider"></div>
      
      <section className="section">
        <div className="container">
          <div className="section-title">
            <h2>Prêt à transformer vos défis scientifiques en opportunités?</h2>
          </div>
          <p className="text-center">Que vous cherchiez à développer une stratégie scientifique internationale, à améliorer votre communication médicale ou à former vos équipes, notre expertise unique est à votre service.</p>
          <div className="text-center" style={{ marginTop: '2rem' }}>
            <Link href="/contact" className="button">Prendre rendez-vous</Link>
          </div>
        </div>
      </section>
      
      <section className="section section-alt">
        <div className="container">
          <div className="section-title">
            <h2>Dernières Publications</h2>
          </div>
          <div className="blog-posts">
            <div className="blog-card">
              <div className="blog-image" style={{ backgroundColor: 'var(--light-green)' }}></div>
              <div className="blog-content">
                <div className="blog-meta">12 Octobre 2023</div>
                <h3>L'IA au service de la recherche scientifique: opportunités et défis</h3>
                <p>Comment l'intelligence artificielle transforme les processus de recherche et ouvre de nouvelles perspectives pour les scientifiques.</p>
                <Link href="/blog/ia-recherche-scientifique">Lire l'article →</Link>
              </div>
            </div>
            <div className="blog-card">
              <div className="blog-image" style={{ backgroundColor: 'var(--light-violet)' }}></div>
              <div className="blog-content">
                <div className="blog-meta">28 Septembre 2023</div>
                <h3>Communication scientifique efficace: traduire la complexité en clarté</h3>
                <p>Stratégies et techniques pour communiquer efficacement des concepts scientifiques complexes à différentes audiences.</p>
                <Link href="/blog/communication-scientifique-efficace">Lire l'article →</Link>
              </div>
            </div>
            <div className="blog-card">
              <div className="blog-image" style={{ backgroundColor: 'var(--light-blue)' }}></div>
              <div className="blog-content">
                <div className="blog-meta">15 Septembre 2023</div>
                <h3>Gestion de réseaux KOL internationaux: bonnes pratiques</h3>
                <p>Comment développer et maintenir des relations fructueuses avec des leaders d'opinion à l'échelle internationale.</p>
                <Link href="/blog/gestion-kol-internationaux">Lire l'article →</Link>
              </div>
            </div>
          </div>
          <div className="text-center" style={{ marginTop: '2rem' }}>
            <Link href="/blog" className="button">Voir toutes les publications</Link>
          </div>
        </div>
      </section>
    </main>
  );
}
