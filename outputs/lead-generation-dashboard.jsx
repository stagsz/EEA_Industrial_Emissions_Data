import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Search, TrendingUp, Users, DollarSign, Award, Download, Play, Settings, Filter, ArrowUpDown, CheckCircle, AlertCircle, Clock } from 'lucide-react';

const LeadGenerationDashboard = () => {
  const [activeStep, setActiveStep] = useState('config');
  const [icpConfig, setIcpConfig] = useState({
    industries: ['Manufacturing', 'Industrial Engineering'],
    companySize: { min: 100, max: 5000 },
    geography: ['Germany', 'Switzerland', 'Austria'],
    revenue: { min: 10000000, max: 500000000 }
  });
  const [leads, setLeads] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searchProgress, setSearchProgress] = useState(0);
  const [filterTier, setFilterTier] = useState('all');
  const [sortBy, setSortBy] = useState('score');
  const [stats, setStats] = useState({
    total: 0,
    tier1: 0,
    tier2: 0,
    tier3: 0,
    avgScore: 0
  });

  // Scoring algorithm based on the skill documentation
  const calculateLeadScore = (lead) => {
    let score = 0;
    
    // Company Fit (35% weight, 0-30 points)
    let companyFit = 0;
    if (icpConfig.industries.includes(lead.industry)) companyFit += 10;
    if (lead.employees >= icpConfig.companySize.min && lead.employees <= icpConfig.companySize.max) companyFit += 10;
    if (icpConfig.geography.some(geo => lead.location.includes(geo))) companyFit += 10;
    score += companyFit;

    // Budget Potential (25% weight, 0-25 points)
    let budgetScore = 0;
    if (lead.revenue >= icpConfig.revenue.min) budgetScore += 15;
    if (lead.growthIndicators) budgetScore += 10;
    score += budgetScore;

    // Decision Maker Quality (20% weight, 0-20 points)
    let dmScore = 0;
    if (lead.contact.title.includes('CEO') || lead.contact.title.includes('Director') || lead.contact.title.includes('VP')) dmScore += 12;
    if (lead.contact.email && lead.contact.email.includes('@')) dmScore += 8;
    score += dmScore;

    // Intent Signals (15% weight, 0-15 points)
    let intentScore = 0;
    if (lead.recentNews) intentScore += 7;
    if (lead.hiring) intentScore += 8;
    score += intentScore;

    // Risk Factors (negative 5%)
    if (lead.riskFactors) score -= 5;

    return Math.min(Math.max(score, 0), 100);
  };

  const getTier = (score) => {
    if (score >= 75) return { tier: 1, label: 'High Priority', color: 'bg-green-500' };
    if (score >= 50) return { tier: 2, label: 'Qualified', color: 'bg-yellow-500' };
    return { tier: 3, label: 'Follow-up', color: 'bg-gray-400' };
  };

  const generateSampleLeads = () => {
    const companies = [
      { name: 'TechForge GmbH', industry: 'Manufacturing', location: 'Munich, Germany', employees: 850, revenue: 45000000 },
      { name: 'Alpine Industries AG', industry: 'Industrial Engineering', location: 'Zurich, Switzerland', employees: 1200, revenue: 78000000 },
      { name: 'Precision Tools Austria', industry: 'Manufacturing', location: 'Vienna, Austria', employees: 450, revenue: 23000000 },
      { name: 'Mechatronics Solutions', industry: 'Industrial Engineering', location: 'Stuttgart, Germany', employees: 2100, revenue: 120000000 },
      { name: 'Swiss Manufacturing Pro', industry: 'Manufacturing', location: 'Basel, Switzerland', employees: 650, revenue: 38000000 },
      { name: 'German Automation Tech', industry: 'Industrial Engineering', location: 'Berlin, Germany', employees: 1800, revenue: 95000000 },
      { name: 'Austrian Precision Works', industry: 'Manufacturing', location: 'Graz, Austria', employees: 320, revenue: 18000000 },
      { name: 'Rhein Industries', industry: 'Manufacturing', location: 'Frankfurt, Germany', employees: 950, revenue: 52000000 },
      { name: 'Helvetic Engineering', industry: 'Industrial Engineering', location: 'Geneva, Switzerland', employees: 780, revenue: 41000000 },
      { name: 'Vienna Tech Solutions', industry: 'Manufacturing', location: 'Vienna, Austria', employees: 560, revenue: 29000000 }
    ];

    const titles = ['CEO', 'VP Operations', 'Director of Manufacturing', 'Head of Engineering', 'Operations Manager', 'Procurement Director'];
    const firstNames = ['Hans', 'Maria', 'Klaus', 'Anna', 'Stefan', 'Julia', 'Michael', 'Sophia'];
    const lastNames = ['Schmidt', 'Müller', 'Weber', 'Meyer', 'Wagner', 'Becker', 'Schulz', 'Hoffmann'];

    return companies.map((company, idx) => {
      const firstName = firstNames[idx % firstNames.length];
      const lastName = lastNames[idx % lastNames.length];
      const domain = company.name.toLowerCase().replace(/\s+/g, '').replace(/[^a-z]/g, '') + '.com';
      
      return {
        id: idx + 1,
        company: company.name,
        industry: company.industry,
        location: company.location,
        employees: company.employees,
        revenue: company.revenue,
        contact: {
          name: `${firstName} ${lastName}`,
          title: titles[idx % titles.length],
          email: `${firstName.toLowerCase()}.${lastName.toLowerCase()}@${domain}`,
          linkedin: `linkedin.com/in/${firstName.toLowerCase()}-${lastName.toLowerCase()}`
        },
        recentNews: Math.random() > 0.5,
        hiring: Math.random() > 0.6,
        growthIndicators: Math.random() > 0.4,
        riskFactors: Math.random() > 0.9,
        discoveryDate: new Date().toISOString().split('T')[0],
        source: 'Web Search'
      };
    });
  };

  const startLeadDiscovery = async () => {
    setIsSearching(true);
    setSearchProgress(0);
    setActiveStep('discovering');
    
    // Simulate progressive lead discovery
    const sampleLeads = generateSampleLeads();
    
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 300));
      setSearchProgress(i);
      
      if (i === 40) {
        // Add first batch of leads
        const batch1 = sampleLeads.slice(0, 4).map(lead => ({
          ...lead,
          score: calculateLeadScore(lead),
          tier: getTier(calculateLeadScore(lead))
        }));
        setLeads(batch1);
      } else if (i === 70) {
        // Add second batch
        const batch2 = sampleLeads.slice(0, 7).map(lead => ({
          ...lead,
          score: calculateLeadScore(lead),
          tier: getTier(calculateLeadScore(lead))
        }));
        setLeads(batch2);
      } else if (i === 100) {
        // Add all leads
        const allLeads = sampleLeads.map(lead => ({
          ...lead,
          score: calculateLeadScore(lead),
          tier: getTier(calculateLeadScore(lead))
        }));
        setLeads(allLeads);
        
        // Calculate stats
        const tier1Count = allLeads.filter(l => l.tier.tier === 1).length;
        const tier2Count = allLeads.filter(l => l.tier.tier === 2).length;
        const tier3Count = allLeads.filter(l => l.tier.tier === 3).length;
        const avgScore = allLeads.reduce((sum, l) => sum + l.score, 0) / allLeads.length;
        
        setStats({
          total: allLeads.length,
          tier1: tier1Count,
          tier2: tier2Count,
          tier3: tier3Count,
          avgScore: Math.round(avgScore)
        });
      }
    }
    
    setIsSearching(false);
    setActiveStep('results');
  };

  const exportToExcel = () => {
    alert('📊 Excel export initiated!\n\nIn a real implementation, this would:\n- Create an .xlsx file with openpyxl\n- Apply conditional formatting (green for Tier 1, yellow for Tier 2, gray for Tier 3)\n- Include all lead data with proper column headers\n- Add a summary sheet with statistics\n- Save to your specified location\n\nFormat: Color-coded by tier, fully formatted, CRM-ready!');
  };

  const filteredLeads = leads.filter(lead => {
    if (filterTier === 'all') return true;
    return lead.tier.tier === parseInt(filterTier);
  });

  const sortedLeads = [...filteredLeads].sort((a, b) => {
    if (sortBy === 'score') return b.score - a.score;
    if (sortBy === 'revenue') return b.revenue - a.revenue;
    if (sortBy === 'employees') return b.employees - a.employees;
    return 0;
  });

  // Chart data
  const tierDistribution = [
    { name: 'Tier 1', value: stats.tier1, color: '#10b981' },
    { name: 'Tier 2', value: stats.tier2, color: '#f59e0b' },
    { name: 'Tier 3', value: stats.tier3, color: '#9ca3af' }
  ];

  const industryData = leads.reduce((acc, lead) => {
    const existing = acc.find(item => item.name === lead.industry);
    if (existing) {
      existing.count++;
    } else {
      acc.push({ name: lead.industry, count: 1 });
    }
    return acc;
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6 border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                🎯 Lead Generation Dashboard
              </h1>
              <p className="text-gray-600">AI-Powered Lead Discovery & Qualification System</p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => setActiveStep('config')}
                className="px-4 py-2 rounded-lg border-2 border-gray-200 hover:border-blue-500 transition-colors flex items-center gap-2"
              >
                <Settings className="w-5 h-5" />
                Configure
              </button>
              {leads.length > 0 && (
                <button
                  onClick={exportToExcel}
                  className="px-6 py-2 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg hover:shadow-lg transition-all flex items-center gap-2 font-semibold"
                >
                  <Download className="w-5 h-5" />
                  Export to Excel
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Configuration Step */}
        {activeStep === 'config' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <Settings className="w-7 h-7 text-blue-600" />
              Configure Your Ideal Customer Profile (ICP)
            </h2>
            
            <div className="grid md:grid-cols-2 gap-6 mb-8">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Target Industries</label>
                <div className="space-y-2">
                  {['Manufacturing', 'Industrial Engineering', 'Technology', 'Healthcare'].map(industry => (
                    <label key={industry} className="flex items-center gap-2 p-3 border rounded-lg hover:bg-blue-50 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={icpConfig.industries.includes(industry)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setIcpConfig({...icpConfig, industries: [...icpConfig.industries, industry]});
                          } else {
                            setIcpConfig({...icpConfig, industries: icpConfig.industries.filter(i => i !== industry)});
                          }
                        }}
                        className="w-4 h-4"
                      />
                      <span>{industry}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Target Geography</label>
                <div className="space-y-2">
                  {['Germany', 'Switzerland', 'Austria', 'Netherlands', 'Belgium'].map(country => (
                    <label key={country} className="flex items-center gap-2 p-3 border rounded-lg hover:bg-blue-50 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={icpConfig.geography.includes(country)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setIcpConfig({...icpConfig, geography: [...icpConfig.geography, country]});
                          } else {
                            setIcpConfig({...icpConfig, geography: icpConfig.geography.filter(g => g !== country)});
                          }
                        }}
                        className="w-4 h-4"
                      />
                      <span>{country}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Company Size (Employees)</label>
                <div className="flex gap-4 items-center">
                  <div className="flex-1">
                    <input
                      type="number"
                      value={icpConfig.companySize.min}
                      onChange={(e) => setIcpConfig({...icpConfig, companySize: {...icpConfig.companySize, min: parseInt(e.target.value)}})}
                      className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                      placeholder="Min"
                    />
                  </div>
                  <span className="text-gray-500">to</span>
                  <div className="flex-1">
                    <input
                      type="number"
                      value={icpConfig.companySize.max}
                      onChange={(e) => setIcpConfig({...icpConfig, companySize: {...icpConfig.companySize, max: parseInt(e.target.value)}})}
                      className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                      placeholder="Max"
                    />
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Annual Revenue ($)</label>
                <div className="flex gap-4 items-center">
                  <div className="flex-1">
                    <input
                      type="number"
                      value={icpConfig.revenue.min}
                      onChange={(e) => setIcpConfig({...icpConfig, revenue: {...icpConfig.revenue, min: parseInt(e.target.value)}})}
                      className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                      placeholder="Min"
                    />
                  </div>
                  <span className="text-gray-500">to</span>
                  <div className="flex-1">
                    <input
                      type="number"
                      value={icpConfig.revenue.max}
                      onChange={(e) => setIcpConfig({...icpConfig, revenue: {...icpConfig.revenue, max: parseInt(e.target.value)}})}
                      className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                      placeholder="Max"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 mb-6">
              <h3 className="font-semibold text-gray-800 mb-3">📋 Your ICP Summary</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Industries</p>
                  <p className="font-bold text-blue-600">{icpConfig.industries.length} selected</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Countries</p>
                  <p className="font-bold text-purple-600">{icpConfig.geography.length} selected</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Company Size</p>
                  <p className="font-bold text-green-600">{icpConfig.companySize.min}-{icpConfig.companySize.max}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Revenue Range</p>
                  <p className="font-bold text-orange-600">${(icpConfig.revenue.min/1000000).toFixed(0)}M+</p>
                </div>
              </div>
            </div>

            <button
              onClick={startLeadDiscovery}
              disabled={isSearching}
              className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-bold text-lg hover:shadow-2xl transition-all flex items-center justify-center gap-3 disabled:opacity-50"
            >
              <Play className="w-6 h-6" />
              Start Lead Discovery
            </button>
          </div>
        )}

        {/* Discovery Step */}
        {activeStep === 'discovering' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <Search className="w-7 h-7 text-blue-600 animate-pulse" />
              Discovering & Qualifying Leads...
            </h2>

            <div className="mb-8">
              <div className="flex justify-between text-sm mb-2">
                <span className="font-semibold">Progress</span>
                <span className="font-bold text-blue-600">{searchProgress}%</span>
              </div>
              <div className="h-4 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-300 rounded-full"
                  style={{ width: `${searchProgress}%` }}
                />
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-4 mb-8">
              <div className={`p-4 rounded-lg border-2 ${searchProgress >= 30 ? 'border-green-500 bg-green-50' : 'border-gray-200'}`}>
                <div className="flex items-center gap-2 mb-2">
                  {searchProgress >= 30 ? <CheckCircle className="w-5 h-5 text-green-600" /> : <Clock className="w-5 h-5 text-gray-400" />}
                  <span className="font-semibold">Web Search</span>
                </div>
                <p className="text-sm text-gray-600">Searching LinkedIn, directories, databases</p>
              </div>

              <div className={`p-4 rounded-lg border-2 ${searchProgress >= 60 ? 'border-green-500 bg-green-50' : 'border-gray-200'}`}>
                <div className="flex items-center gap-2 mb-2">
                  {searchProgress >= 60 ? <CheckCircle className="w-5 h-5 text-green-600" /> : <Clock className="w-5 h-5 text-gray-400" />}
                  <span className="font-semibold">AI Qualification</span>
                </div>
                <p className="text-sm text-gray-600">Scoring leads with 5-factor model</p>
              </div>

              <div className={`p-4 rounded-lg border-2 ${searchProgress >= 90 ? 'border-green-500 bg-green-50' : 'border-gray-200'}`}>
                <div className="flex items-center gap-2 mb-2">
                  {searchProgress >= 90 ? <CheckCircle className="w-5 h-5 text-green-600" /> : <Clock className="w-5 h-5 text-gray-400" />}
                  <span className="font-semibold">Data Enrichment</span>
                </div>
                <p className="text-sm text-gray-600">Adding contact info & verification</p>
              </div>
            </div>

            {leads.length > 0 && (
              <div className="bg-blue-50 rounded-xl p-6">
                <h3 className="font-semibold text-gray-800 mb-4">🔥 Live Results</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center">
                    <p className="text-3xl font-bold text-blue-600">{leads.length}</p>
                    <p className="text-sm text-gray-600">Leads Found</p>
                  </div>
                  <div className="text-center">
                    <p className="text-3xl font-bold text-green-600">{leads.filter(l => l.tier.tier === 1).length}</p>
                    <p className="text-sm text-gray-600">Tier 1</p>
                  </div>
                  <div className="text-center">
                    <p className="text-3xl font-bold text-purple-600">{Math.round(leads.reduce((sum, l) => sum + l.score, 0) / leads.length)}</p>
                    <p className="text-sm text-gray-600">Avg Score</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Results Step */}
        {activeStep === 'results' && (
          <>
            {/* Stats Dashboard */}
            <div className="grid md:grid-cols-4 gap-6 mb-6">
              <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
                <div className="flex items-center justify-between mb-3">
                  <Users className="w-10 h-10 text-blue-500" />
                  <span className="text-3xl font-bold text-gray-800">{stats.total}</span>
                </div>
                <p className="text-gray-600 font-semibold">Total Leads</p>
              </div>

              <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg p-6 text-white">
                <div className="flex items-center justify-between mb-3">
                  <Award className="w-10 h-10" />
                  <span className="text-3xl font-bold">{stats.tier1}</span>
                </div>
                <p className="font-semibold">Tier 1 (High Priority)</p>
              </div>

              <div className="bg-gradient-to-br from-yellow-500 to-orange-600 rounded-xl shadow-lg p-6 text-white">
                <div className="flex items-center justify-between mb-3">
                  <TrendingUp className="w-10 h-10" />
                  <span className="text-3xl font-bold">{stats.tier2}</span>
                </div>
                <p className="font-semibold">Tier 2 (Qualified)</p>
              </div>

              <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
                <div className="flex items-center justify-between mb-3">
                  <DollarSign className="w-10 h-10 text-purple-500" />
                  <span className="text-3xl font-bold text-gray-800">{stats.avgScore}</span>
                </div>
                <p className="text-gray-600 font-semibold">Average Score</p>
              </div>
            </div>

            {/* Charts */}
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
                <h3 className="text-lg font-bold mb-4">Lead Distribution by Tier</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={tierDistribution}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${value}`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {tierDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
                <h3 className="text-lg font-bold mb-4">Leads by Industry</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={industryData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#8b5cf6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Leads Table */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold">Qualified Leads</h3>
                <div className="flex gap-3">
                  <select
                    value={filterTier}
                    onChange={(e) => setFilterTier(e.target.value)}
                    className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="all">All Tiers</option>
                    <option value="1">Tier 1 Only</option>
                    <option value="2">Tier 2 Only</option>
                    <option value="3">Tier 3 Only</option>
                  </select>

                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                    className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="score">Sort by Score</option>
                    <option value="revenue">Sort by Revenue</option>
                    <option value="employees">Sort by Size</option>
                  </select>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b-2 border-gray-200">
                      <th className="text-left p-3 font-semibold">Tier</th>
                      <th className="text-left p-3 font-semibold">Score</th>
                      <th className="text-left p-3 font-semibold">Company</th>
                      <th className="text-left p-3 font-semibold">Industry</th>
                      <th className="text-left p-3 font-semibold">Location</th>
                      <th className="text-left p-3 font-semibold">Contact</th>
                      <th className="text-left p-3 font-semibold">Title</th>
                      <th className="text-left p-3 font-semibold">Email</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sortedLeads.map((lead) => (
                      <tr key={lead.id} className="border-b hover:bg-gray-50">
                        <td className="p-3">
                          <span className={`px-3 py-1 rounded-full text-white text-xs font-bold ${lead.tier.color}`}>
                            T{lead.tier.tier}
                          </span>
                        </td>
                        <td className="p-3">
                          <span className="font-bold text-lg">{lead.score}</span>
                        </td>
                        <td className="p-3 font-semibold">{lead.company}</td>
                        <td className="p-3 text-sm text-gray-600">{lead.industry}</td>
                        <td className="p-3 text-sm text-gray-600">{lead.location}</td>
                        <td className="p-3">{lead.contact.name}</td>
                        <td className="p-3 text-sm text-gray-600">{lead.contact.title}</td>
                        <td className="p-3">
                          <a href={`mailto:${lead.contact.email}`} className="text-blue-600 hover:underline text-sm">
                            {lead.contact.email}
                          </a>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default LeadGenerationDashboard;