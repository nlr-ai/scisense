import React from 'react';
import './globals.css';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export const metadata = {
  title: 'SciSense - Making Science make sense',
  description: 'Expertise en stratégies médico-scientifiques internationales, gestion de réseaux KOL et applications d\'IA pour la recherche scientifique',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet" />
        <link rel="icon" type="image/png" href="/assets/images/favicon.png" />
      </head>
      <body>
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  );
}
