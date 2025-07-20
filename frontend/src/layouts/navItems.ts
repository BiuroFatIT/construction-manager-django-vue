// src/layouts/navigation.js
export const navItems = [
    { header: '' },
    { header: 'Główne' },
    { title: 'Strona główna', icon: 'mdi-home-outline', to: '/' },
  
    { header: 'Moduły' },
    {
      title: 'Firmy',
      icon: 'mdi-account-group',
      children: [
        { title: 'Lista Firm', to: '/company/list', icon: 'mdi-format-list-bulleted' },
      ],
    },
    {
      title: 'Ekipy',
      icon: 'mdi-account-group',
      children: [
        { title: 'Lista ekip', to: '/teams/list', icon: 'mdi-format-list-bulleted' },
        { title: 'Karta ekipy', to: '/teams/card', icon: 'mdi-card-account-details' },
        { title: 'CRUD ekipy', to: '/teams/crud', icon: 'mdi-account-edit' },
        { title: 'Typy ekip', to: '/teams/types', icon: 'mdi-account-group-outline' },
      ],
    },
    {
      title: 'Produkty',
      icon: 'mdi-package-variant',
      children: [
        { title: 'Lista produktów', to: '/products/list', icon: 'mdi-format-list-bulleted' },
        { title: 'CRUD produktu', to: '/products/crud', icon: 'mdi-package-variant-closed' },
      ],
    },
    {
      title: 'Klienci',
      icon: 'mdi-account-multiple',
      children: [
        { title: 'Lista klientów', to: '/clients/list', icon: 'mdi-format-list-bulleted' },
        { title: 'CRUD klienta', to: '/clients/crud', icon: 'mdi-account-edit' },
      ],
    },
    {
      title: 'Etapy budowy',
      icon: 'mdi-domain',
      children: [
        { title: 'Lista etapów', to: '/stages/list', icon: 'mdi-format-list-bulleted' },
        { title: 'CRUD etapów', to: '/stages/crud', icon: 'mdi-domain-edit' },
      ],
    },
  
    { header: 'Harmonogramy' },
    { title: 'Kalendarz ekip', icon: 'mdi-calendar-clock', to: '/calendar/teams' },
    { title: 'Kalendarz inwestycji', icon: 'mdi-calendar-multiple', to: '/calendar/investments' },
  
    { header: 'Mapy' },
    { title: 'Mapa budowy', icon: 'mdi-map', to: '/map/overview' },
    { title: 'Lokalizacja ekip', icon: 'mdi-map-marker', to: '/map/teams' },

  ]
  