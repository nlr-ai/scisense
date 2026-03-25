import React from 'react';
import Link from 'next/link';

export default function Blog() {
  return (
    <main>
      <section className="hero" style={{ padding: '4rem 0' }}>
        <div className="container">
          <h1>Blog</h1>
          <p className="hero-tagline">Réflexions et analyses sur les affaires scientifiques et médicales</p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="section-title">
            <h2>Articles Récents</h2>
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
            
            <div className="blog-card">
              <div className="blog-image" style={{ backgroundColor: 'var(--primary-violet)', opacity: 0.7 }}></div>
              <div className="blog-content">
                <div className="blog-meta">2 Septembre 2023</div>
                <h3>Stratégies médico-scientifiques internationales: adapter sans dénaturer</h3>
                <p>Comment maintenir la cohérence de votre message scientifique tout en l'adaptant aux spécificités locales.</p>
                <Link href="/blog/strategies-medico-scientifiques-internationales">Lire l'article →</Link>
              </div>
            </div>
            
            <div className="blog-card">
              <div className="blog-image" style={{ backgroundColor: 'var(--secondary-blue)', opacity: 0.7 }}></div>
              <div className="blog-content">
                <div className="blog-meta">18 Août 2023</div>
                <h3>L'importance de la formation médicale pour les équipes commerciales</h3>
                <p>Pourquoi et comment investir dans la formation scientifique de vos équipes commerciales pour maximiser leur impact.</p>
                <Link href="/blog/formation-medicale-equipes-commerciales">Lire l'article →</Link>
              </div>
            </div>
            
            <div className="blog-card">
              <div className="blog-image" style={{ backgroundColor: 'var(--accent-green)', opacity: 0.7 }}></div>
              <div className="blog-content">
                <div className="blog-meta">5 Août 2023</div>
                <h3>Du laboratoire au marché: le parcours d'une innovation scientifique</h3>
                <p>Les étapes clés pour transformer une découverte scientifique en produit commercialisable avec succès.</p>
                <Link href="/blog/laboratoire-au-marche">Lire l'article →</Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section section-alt">
        <div className="container">
          <div className="section-title">
            <h2>Catégories</h2>
          </div>
          
          <div className="services" style={{ marginBottom: '2rem' }}>
            <div className="service-card">
              <h3>Communication Scientifique</h3>
              <p>Articles sur les meilleures pratiques pour communiquer efficacement des concepts scientifiques complexes.</p>
              <Link href="/blog/category/communication-scientifique">Voir les articles →</Link>
            </div>
            
            <div className="service-card">
              <h3>Intelligence Artificielle</h3>
              <p>Analyses des applications de l'IA dans la recherche scientifique et les affaires médicales.</p>
              <Link href="/blog/category/intelligence-artificielle">Voir les articles →</Link>
            </div>
            
            <div className="service-card">
              <h3>Stratégies Internationales</h3>
              <p>Réflexions sur le déploiement de stratégies médico-scientifiques à l'échelle internationale.</p>
              <Link href="/blog/category/strategies-internationales">Voir les articles →</Link>
            </div>
            
            <div className="service-card">
              <h3>Gestion de KOL</h3>
              <p>Conseils et analyses sur la création et l'animation de réseaux d'experts médicaux.</p>
              <Link href="/blog/category/gestion-kol">Voir les articles →</Link>
            </div>
          </div>
          
          <div className="text-center">
            <p>Consultez régulièrement notre blog pour découvrir nos derniers articles et analyses.</p>
            <Link href="/contact" className="button">Nous contacter</Link>
          </div>
        </div>
      </section>

      {/* Client-side script for animations */}
      <script dangerouslySetInnerHTML={{
        __html: `
          document.addEventListener('DOMContentLoaded', function() {
            // Add animation to blog cards when they come into view
            const blogCards = document.querySelectorAll('.blog-card');
            
            const observer = new IntersectionObserver((entries) => {
              entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                  setTimeout(() => {
                    entry.target.style.opacity = 1;
                    entry.target.style.transform = 'translateY(0)';
                  }, index * 100); // Staggered animation
                }
              });
            }, { threshold: 0.1 });
            
            blogCards.forEach(card => {
              card.style.opacity = 0;
              card.style.transform = 'translateY(20px)';
              card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
              observer.observe(card);
            });
            
            // Add animation to service cards
            const serviceCards = document.querySelectorAll('.service-card');
            
            const cardObserver = new IntersectionObserver((entries) => {
              entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                  setTimeout(() => {
                    entry.target.style.opacity = 1;
                    entry.target.style.transform = 'translateY(0)';
                  }, index * 100); // Staggered animation
                }
              });
            }, { threshold: 0.1 });
            
            serviceCards.forEach(card => {
              card.style.opacity = 0;
              card.style.transform = 'translateY(20px)';
              card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
              cardObserver.observe(card);
            });
          });
        `
      }} />
    </main>
  );
}
