import React, { useState, useEffect } from 'react';
import { FaSearch, FaFilter, FaSort, FaStar, FaCheckCircle, FaMapMarkerAlt, FaPhone, FaClock, FaTruck, FaRobot, FaStore, FaFlask, FaMedkit, FaClinicMedical } from 'react-icons/fa';
import Header from '../components/Header';

const StoreBrowserPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sortBy, setSortBy] = useState('nearest');
  const [viewMode, setViewMode] = useState('grid');
  const [filters, setFilters] = useState({
    openNow: false,
    verified: true,
    delivery: false
  });
  const [visibleStores, setVisibleStores] = useState(9);

  const categories = [
    { id: 'all', label: 'All', icon: FaStore },
    { id: 'pharmacy', label: 'Pharmacy', icon: FaMedkit },
    { id: 'lab', label: 'Diagnostics', icon: FaFlask },
    { id: 'clinic', label: 'Clinic', icon: FaClinicMedical },
    { id: 'supplies', label: 'Supplies', icon: FaMedkit },
    { id: 'vaccines', label: 'Vaccines', icon: FaClinicMedical }
  ];

  const stores = [
    {
      id: 1,
      name: 'City Central Pharmacy',
      type: 'Pharmacy',
      category: 'pharmacy',
      rating: 4.8,
      verified: true,
      image: '/api/placeholder/150/100',
      distance: '1.2 km',
      availability: ['Insulin available', 'Blood pressure meds'],
      openNow: true,
      delivery: true,
      phone: '+1 (555) 123-4567',
      address: '123 Health St, Downtown'
    },
    {
      id: 2,
      name: 'Oak Valley Hospital Lab',
      type: 'Diagnostics',
      category: 'lab',
      rating: 4.9,
      verified: true,
      image: '/api/placeholder/150/100',
      distance: '2.8 km',
      availability: ['Malaria test kits low', 'COVID-19 testing'],
      openNow: true,
      delivery: false,
      phone: '+1 (555) 987-6543',
      address: '456 Wellness Ave, Medical District'
    },
    {
      id: 3,
      name: 'MediSupply Plus',
      type: 'Equipment Supplier',
      category: 'supplies',
      rating: 4.6,
      verified: true,
      image: '/api/placeholder/150/100',
      distance: '3.5 km',
      availability: ['Wheelchairs', 'Oxygen tanks'],
      openNow: false,
      delivery: true,
      phone: '+1 (555) 456-7890',
      address: '789 Cure Blvd, Industrial Park'
    },
    {
      id: 4,
      name: 'Downtown Diagnostics',
      type: 'Lab',
      category: 'lab',
      rating: 4.7,
      verified: true,
      image: '/api/placeholder/150/100',
      distance: '0.8 km',
      availability: ['Blood tests', 'X-ray services'],
      openNow: true,
      delivery: false,
      phone: '+1 (555) 321-0987',
      address: '321 Medical Plaza, Downtown'
    },
    {
      id: 5,
      name: 'Green Valley Clinic',
      type: 'Clinic',
      category: 'clinic',
      rating: 4.9,
      verified: true,
      image: '/api/placeholder/150/100',
      distance: '4.1 km',
      availability: ['General practice', 'Vaccinations'],
      openNow: true,
      delivery: false,
      phone: '+1 (555) 654-3210',
      address: '654 Healing Way, Suburban'
    },
    {
      id: 6,
      name: 'PharmaCare Express',
      type: 'Pharmacy',
      category: 'pharmacy',
      rating: 4.5,
      verified: true,
      image: '/api/placeholder/150/100',
      distance: '1.9 km',
      availability: ['Antibiotics', 'Pain medication'],
      openNow: true,
      delivery: true,
      phone: '+1 (555) 789-0123',
      address: '987 Wellness Dr, Midtown'
    }
  ];

  const filteredStores = stores
    .filter(store => {
      const matchesSearch = store.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           store.type.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesCategory = selectedCategory === 'all' || store.category === selectedCategory;
      const matchesFilters = (!filters.openNow || store.openNow) &&
                            (!filters.verified || store.verified) &&
                            (!filters.delivery || store.delivery);
      return matchesSearch && matchesCategory && matchesFilters;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'nearest':
          return parseFloat(a.distance) - parseFloat(b.distance);
        case 'rating':
          return b.rating - a.rating;
        case 'newest':
          return b.id - a.id;
        default:
          return 0;
      }
    });

  const displayedStores = filteredStores.slice(0, visibleStores);

  const loadMore = () => {
    setVisibleStores(prev => prev + 9);
  };

  const handleFilterChange = (filterName) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: !prev[filterName]
    }));
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />

      {/* Top Bar */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            {/* Search Bar */}
            <div className="flex-1 max-w-md">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FaSearch className="text-gray-400" />
                </div>
                <input
                  type="text"
                  placeholder="Search for a pharmacy, lab, or vendor..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center gap-3">
              <button className="flex items-center px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                <FaFilter className="mr-2 text-gray-600" />
                Filters
              </button>

              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="nearest">Nearest</option>
                <option value="rating">Rating</option>
                <option value="newest">Newest</option>
              </select>

              <div className="flex border border-gray-300 rounded-lg">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-3 py-2 ${viewMode === 'grid' ? 'bg-blue-50 text-blue-600' : 'text-gray-600'} rounded-l-lg`}
                >
                  Grid
                </button>
                <button
                  onClick={() => setViewMode('map')}
                  className={`px-3 py-2 ${viewMode === 'map' ? 'bg-blue-50 text-blue-600' : 'text-gray-600'} rounded-r-lg`}
                >
                  Map
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex gap-8">
          {/* Sidebar */}
          <div className="hidden lg:block w-64 flex-shrink-0">
            <div className="bg-gray-50 rounded-lg p-6 sticky top-24">
              <h3 className="font-semibold text-gray-800 mb-4">Filters</h3>

              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={filters.openNow}
                    onChange={() => handleFilterChange('openNow')}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700 flex items-center">
                    <FaClock className="mr-1 text-green-500" />
                    Open Now
                  </span>
                </label>

                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={filters.verified}
                    onChange={() => handleFilterChange('verified')}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700 flex items-center">
                    <FaCheckCircle className="mr-1 text-blue-500" />
                    Verified Vendors
                  </span>
                </label>

                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={filters.delivery}
                    onChange={() => handleFilterChange('delivery')}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700 flex items-center">
                    <FaTruck className="mr-1 text-emerald-500" />
                    Delivery Available
                  </span>
                </label>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            {/* Category Tabs */}
            <div className="flex flex-wrap gap-2 mb-6">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`flex items-center px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    selectedCategory === category.id
                      ? 'bg-blue-100 text-blue-800 border border-blue-200'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <category.icon className="mr-2" />
                  {category.label}
                </button>
              ))}
            </div>

            {/* Results Count */}
            <div className="mb-6">
              <p className="text-gray-600">
                Showing {displayedStores.length} of {filteredStores.length} stores
              </p>
            </div>

            {/* Store Grid */}
            <div className={`grid gap-6 ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 xl:grid-cols-3' : 'grid-cols-1'}`}>
              {displayedStores.map((store, index) => (
                <div
                  key={store.id}
                  className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 animate-fade-in"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center">
                      <img
                        src={store.image}
                        alt={store.name}
                        className="w-12 h-12 rounded-lg object-cover mr-3"
                      />
                      <div>
                        <h3 className="font-semibold text-gray-800">{store.name}</h3>
                        <p className="text-sm text-gray-600">{store.type}</p>
                      </div>
                    </div>
                    {store.verified && (
                      <FaCheckCircle className="text-blue-500 text-lg" />
                    )}
                  </div>

                  <div className="flex items-center mb-3">
                    <div className="flex items-center mr-4">
                      {[...Array(5)].map((_, i) => (
                        <FaStar
                          key={i}
                          className={`text-sm ${i < Math.floor(store.rating) ? 'text-yellow-400' : 'text-gray-300'}`}
                        />
                      ))}
                      <span className="ml-1 text-sm text-gray-600">{store.rating}</span>
                    </div>
                    <span className="text-sm text-gray-500">{store.distance}</span>
                  </div>

                  <div className="mb-4">
                    {store.availability.slice(0, 2).map((item, idx) => (
                      <span
                        key={idx}
                        className="inline-block bg-emerald-100 text-emerald-800 text-xs px-2 py-1 rounded-full mr-2 mb-2"
                      >
                        {item}
                      </span>
                    ))}
                  </div>

                  <div className="flex items-center justify-between">
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
                      View Store
                    </button>
                    <div className="flex items-center text-xs text-gray-500">
                      {store.openNow && <FaClock className="mr-1 text-green-500" />}
                      {store.delivery && <FaTruck className="ml-2 text-emerald-500" />}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Load More */}
            {visibleStores < filteredStores.length && (
              <div className="text-center mt-8">
                <button
                  onClick={loadMore}
                  className="bg-gray-100 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-200 transition-colors"
                >
                  Load More Stores
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* AI Suggestion Bar */}
      <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2 bg-white border border-gray-200 rounded-full px-6 py-3 shadow-lg">
        <div className="flex items-center">
          <FaRobot className="text-blue-500 mr-3" />
          <span className="text-sm text-gray-700">
            We found <strong>3 nearby pharmacies</strong> with your last prescription in stock.
          </span>
          <button className="ml-4 bg-blue-600 text-white px-4 py-1 rounded-full text-xs font-medium hover:bg-blue-700 transition-colors">
            View
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-50 border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <div className="flex items-center justify-center mb-4">
              <FaCheckCircle className="text-blue-500 mr-2" />
              <span className="text-sm text-gray-600">
                MedVault verifies all listed vendors for compliance and reliability.
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default StoreBrowserPage;
