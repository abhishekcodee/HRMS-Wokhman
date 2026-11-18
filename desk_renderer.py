import os

DESK_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Frappe HR - Desk</title>
  <link rel="icon" href="/assets/frappe/images/frappe-favicon.svg" type="image/x-icon">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
  <style>
    :root {
      --bg-surface: #f9fafb;
      --bg-card: #ffffff;
      --border-color: #e5e7eb;
      --text-main: #111827;
      --text-muted: #6b7280;
      --primary: #1f2937;
      --primary-hover: #111827;
      --blue-accent: #2563eb;
      --cyan-badge-bg: #ecfeff;
      --cyan-badge-text: #0891b2;
      --sidebar-width: 240px;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    body {
      background-color: var(--bg-surface);
      color: var(--text-main);
      display: flex;
      height: 100vh;
      overflow: hidden;
      font-size: 13px;
    }
    /* Left Sidebar */
    .sidebar {
      width: var(--sidebar-width);
      background-color: #ffffff;
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      user-select: none;
    }
    .sidebar-header {
      padding: 14px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border-color);
    }
    .brand-group {
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
    }
    .brand-logo {
      width: 28px;
      height: 28px;
      background: #0284c7;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-weight: 700;
      font-size: 16px;
    }
    .brand-title {
      font-size: 14px;
      font-weight: 600;
      color: #1f2937;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .brand-title svg {
      width: 14px;
      height: 14px;
      color: var(--text-muted);
    }
    .sidebar-nav {
      flex: 1;
      overflow-y: auto;
      padding: 12px 8px;
    }
    .nav-section-title {
      font-size: 11px;
      font-weight: 600;
      color: #9ca3af;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 8px 12px 4px;
    }
    .nav-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 7px 12px;
      border-radius: 6px;
      color: #374151;
      text-decoration: none;
      cursor: pointer;
      font-size: 13px;
      font-weight: 450;
      transition: background 0.15s ease;
      margin-bottom: 2px;
    }
    .nav-item:hover {
      background-color: #f3f4f6;
      color: #111827;
    }
    .nav-item.active {
      background-color: #e5e7eb;
      color: #111827;
      font-weight: 600;
    }
    .nav-item svg {
      width: 16px;
      height: 16px;
      color: #6b7280;
      flex-shrink: 0;
    }
    .nav-subgroup {
      margin-left: 20px;
      border-left: 1px solid #e5e7eb;
      padding-left: 8px;
      margin-top: 2px;
      margin-bottom: 4px;
    }
    .nav-subitem {
      display: block;
      padding: 5px 10px;
      border-radius: 5px;
      color: #4b5563;
      text-decoration: none;
      font-size: 13px;
      cursor: pointer;
      margin-bottom: 2px;
    }
    .nav-subitem:hover {
      background-color: #f3f4f6;
      color: #111827;
    }
    .nav-subitem.active {
      background-color: #f3f4f6;
      color: #0284c7;
      font-weight: 600;
    }
    .sidebar-footer {
      padding: 12px 14px;
      border-top: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #fafafa;
    }
    .user-pill {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }
    .avatar-circle {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: #f43f5e;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 11px;
    }
    .user-name {
      font-weight: 500;
      font-size: 12px;
      color: #1f2937;
    }
    .pwa-link-btn {
      padding: 4px 8px;
      border: 1px solid #d1d5db;
      background: #fff;
      border-radius: 4px;
      font-size: 11px;
      color: #374151;
      text-decoration: none;
      cursor: pointer;
    }
    .pwa-link-btn:hover {
      background: #f3f4f6;
    }
    /* Main Content Area */
    .main-wrapper {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background: #ffffff;
    }
    .top-bar {
      height: 52px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      background: #ffffff;
    }
    .top-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .page-title {
      font-size: 16px;
      font-weight: 600;
      color: #111827;
    }
    .top-right {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .view-select {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 10px;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      font-size: 12px;
      color: #374151;
      background: #fff;
      cursor: pointer;
    }
    .icon-btn {
      width: 30px;
      height: 30px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      background: #fff;
      color: #4b5563;
      cursor: pointer;
      transition: background 0.15s ease;
    }
    .icon-btn:hover {
      background: #f3f4f6;
    }
    .icon-btn svg {
      width: 14px;
      height: 14px;
    }
    .btn-primary {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      background: #111827;
      color: #ffffff;
      border: none;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: background 0.15s ease;
    }
    .btn-primary:hover {
      background: #000000;
    }
    /* Filter Bar */
    .filter-bar {
      padding: 10px 20px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      background: #ffffff;
    }
    .filter-inputs {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 1;
    }
    .filter-input-wrap {
      display: flex;
      align-items: center;
      background: #f3f4f6;
      border-radius: 6px;
      padding: 4px 8px;
      font-size: 12px;
      color: #4b5563;
      width: 220px;
    }
    .filter-input-wrap span {
      color: #9ca3af;
      margin-right: 6px;
    }
    .filter-input-wrap input {
      border: none;
      background: transparent;
      outline: none;
      width: 100%;
      font-size: 12px;
      color: #111827;
    }
    .filter-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .filter-btn {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 5px 10px;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      background: #fff;
      font-size: 12px;
      color: #374151;
      cursor: pointer;
    }
    .filter-btn:hover {
      background: #f3f4f6;
    }
    /* Table Container */
    .table-container {
      flex: 1;
      overflow-y: auto;
      background: #ffffff;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }
    thead th {
      position: sticky;
      top: 0;
      background: #fafafa;
      border-bottom: 1px solid var(--border-color);
      padding: 8px 14px;
      font-size: 12px;
      font-weight: 500;
      color: #6b7280;
      white-space: nowrap;
      user-select: none;
    }
    tbody tr {
      border-bottom: 1px solid #f3f4f6;
      transition: background 0.1s ease;
      cursor: pointer;
    }
    tbody tr:hover {
      background-color: #f9fafb;
    }
    tbody td {
      padding: 9px 14px;
      font-size: 13px;
      color: #1f2937;
      vertical-align: middle;
      white-space: nowrap;
    }
    .td-id {
      font-weight: 500;
      color: #111827;
    }
    .status-badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 500;
      background: var(--cyan-badge-bg);
      color: var(--cyan-badge-text);
    }
    .check-icon {
      color: #4b5563;
      font-size: 14px;
    }
    .meta-icons {
      display: flex;
      align-items: center;
      gap: 12px;
      color: #9ca3af;
      font-size: 12px;
    }
    .meta-icons svg {
      width: 14px;
      height: 14px;
      cursor: pointer;
    }
    .meta-icons svg:hover {
      color: #4b5563;
    }
    /* Pagination Footer */
    .table-footer {
      height: 44px;
      border-top: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      background: #ffffff;
      font-size: 12px;
      color: #6b7280;
    }
    .page-sizes {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .page-size-btn {
      padding: 2px 8px;
      border-radius: 4px;
      cursor: pointer;
      color: #6b7280;
    }
    .page-size-btn.active {
      background: #f3f4f6;
      color: #111827;
      font-weight: 600;
    }
    /* Modal */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.4);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    .modal-overlay.open {
      display: flex;
    }
    .modal-card {
      background: #ffffff;
      width: 500px;
      max-width: 90vw;
      border-radius: 10px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
      overflow: hidden;
      animation: modalFade 0.15s ease-out;
    }
    @keyframes modalFade {
      from { transform: scale(0.96); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }
    .modal-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .modal-title {
      font-size: 15px;
      font-weight: 600;
      color: #111827;
    }
    .modal-body {
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .form-label {
      font-size: 12px;
      font-weight: 500;
      color: #374151;
    }
    .form-control {
      padding: 8px 12px;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      font-size: 13px;
      color: #111827;
      outline: none;
    }
    .form-control:focus {
      border-color: #0284c7;
    }
    .form-check {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 4px;
      font-size: 13px;
      color: #374151;
      cursor: pointer;
    }
    .modal-footer {
      padding: 14px 20px;
      border-top: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 10px;
      background: #fafafa;
    }
    .btn-secondary {
      padding: 6px 14px;
      border: 1px solid var(--border-color);
      background: #ffffff;
      border-radius: 6px;
      font-size: 13px;
      color: #374151;
      cursor: pointer;
    }
    .btn-secondary:hover {
      background: #f3f4f6;
    }
  </style>
</head>
<body>

  <!-- Left Sidebar -->
  <aside class="sidebar">
    <div class="sidebar-header">
      <div class="brand-group" onclick="switchDocType('Department')">
        <div class="brand-logo">E</div>
        <div class="brand-title">
          Setup
          <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg>
        </div>
      </div>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-section-title">Navigation</div>
      <div class="nav-item" onclick="switchDocType('Home')">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
        Home
      </div>
      <div class="nav-item" onclick="switchDocType('Company')">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
        Company
      </div>
      <div class="nav-item" onclick="switchDocType('User')">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
        Users
      </div>

      <!-- Organization Section -->
      <div class="nav-item active" style="font-weight: 600;">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h7"></path></svg>
        Organization
      </div>
      <div class="nav-subgroup">
        <div class="nav-subitem" id="nav-Branch" onclick="switchDocType('Branch')">Branch</div>
        <div class="nav-subitem active" id="nav-Department" onclick="switchDocType('Department')">Department</div>
        <div class="nav-subitem" id="nav-Designation" onclick="switchDocType('Designation')">Designation</div>
        <div class="nav-subitem" id="nav-Holiday List" onclick="switchDocType('Holiday List')">Holiday List</div>
      </div>

      <div class="nav-section-title">HR & Operations</div>
      <div class="nav-item" id="nav-Employee" onclick="switchDocType('Employee')">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
        Employees
      </div>
      <div class="nav-item" id="nav-Attendance" onclick="switchDocType('Attendance')">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
        Attendance
      </div>
      <div class="nav-item" id="nav-Leave Application" onclick="switchDocType('Leave Application')">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        Leaves
      </div>
      <div class="nav-item" id="nav-Expense Claim" onclick="switchDocType('Expense Claim')">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
        Expense Claims
      </div>
      <div class="nav-item" id="nav-Shift Type" onclick="switchDocType('Shift Type')">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
        Shift Types
      </div>

      <div class="nav-section-title">System Settings</div>
      <div class="nav-item" onclick="switchDocType('System Settings')">
        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
        System Settings
      </div>
    </nav>

    <div class="sidebar-footer">
      <div class="user-pill" title="Administrator">
        <div class="avatar-circle">AU</div>
        <div class="user-name">Abhishek</div>
      </div>
      <a href="/hrms" class="pwa-link-btn" title="Open Employee PWA">PWA View</a>
    </div>
  </aside>

  <!-- Main View -->
  <main class="main-wrapper">
    <!-- Top Header -->
    <div class="top-bar">
      <div class="top-left">
        <h1 class="page-title" id="current-title">Department</h1>
      </div>
      <div class="top-right">
        <div class="view-select">
          <span>List View</span>
          <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg>
        </div>
        <button class="icon-btn" onclick="loadDocTypeData()" title="Reload">
          <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
        </button>
        <button class="icon-btn" title="Menu">
          <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"></path></svg>
        </button>
        <button class="btn-primary" id="btn-add-primary" onclick="openAddModal()">
          <span id="btn-add-text">+ Add Department</span>
          <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg>
        </button>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="filter-inputs">
        <div class="filter-input-wrap">
          <span>ID</span>
          <span>≈</span>
          <input type="text" id="filter-id" placeholder="" oninput="applyClientFilter()">
        </div>
        <div class="filter-input-wrap">
          <span>Company</span>
          <input type="text" id="filter-company" placeholder="" oninput="applyClientFilter()">
        </div>
      </div>
      <div class="filter-actions">
        <button class="filter-btn">
          <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
          Filter
        </button>
        <button class="filter-btn">
          Created On
          <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg>
        </button>
      </div>
    </div>

    <!-- Data Table -->
    <div class="table-container">
      <table id="records-table">
        <thead id="table-head">
          <!-- Dynamically populated -->
        </thead>
        <tbody id="table-body">
          <!-- Dynamically populated -->
        </tbody>
      </table>
    </div>

    <!-- Pagination Footer -->
    <div class="table-footer">
      <div class="page-sizes">
        <span class="page-size-btn active">20</span>
        <span class="page-size-btn">100</span>
        <span class="page-size-btn">500</span>
        <span class="page-size-btn">2500</span>
      </div>
      <div id="footer-count">0 of 0</div>
    </div>
  </main>

  <!-- Add Record Modal -->
  <div class="modal-overlay" id="add-modal">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title" id="modal-title">New Department</h3>
        <button class="icon-btn" onclick="closeAddModal()" style="border:none;">✕</button>
      </div>
      <div class="modal-body" id="modal-form-fields">
        <!-- Dynamically rendered based on active DocType -->
      </div>
      <div class="modal-footer">
        <button class="btn-secondary" onclick="closeAddModal()">Cancel</button>
        <button class="btn-primary" onclick="submitNewRecord()">Save</button>
      </div>
    </div>
  </div>

  <script>
    let currentDocType = "Department";
    let recordsData = [];
    let parentDepartmentsList = [];
    let companiesList = [];

    // Initialize from URL path
    function initRoute() {
      const path = window.location.pathname.toLowerCase();
      if (path.includes("designation")) {
        switchDocType("Designation");
      } else if (path.includes("branch")) {
        switchDocType("Branch");
      } else if (path.includes("employee")) {
        switchDocType("Employee");
      } else if (path.includes("company")) {
        switchDocType("Company");
      } else if (path.includes("user")) {
        switchDocType("User");
      } else if (path.includes("holiday")) {
        switchDocType("Holiday List");
      } else {
        switchDocType("Department");
      }
    }

    function switchDocType(doctype) {
      if (doctype === "Home") {
        window.location.href = "/hrms/home";
        return;
      }
      currentDocType = doctype;
      document.getElementById("current-title").innerText = doctype;
      document.getElementById("btn-add-text").innerText = `+ Add ${doctype}`;
      
      // Update sidebar subitem highlighting
      document.querySelectorAll(".nav-subitem, .nav-item").forEach(el => el.classList.remove("active"));
      const activeEl = document.getElementById(`nav-${doctype}`);
      if (activeEl) activeEl.classList.add("active");

      // Update URL without page reload
      window.history.pushState({}, "", `/app/${doctype.toLowerCase().replace(/\\s+/g, "-")}`);

      loadDocTypeData();
    }

    async function loadDocTypeData() {
      try {
        const res = await fetch("/api/method/frappe.client.get_list", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ doctype: currentDocType, limit: 100 })
        });
        const json = await res.json();
        recordsData = json.message || [];
        renderTable(recordsData);
      } catch (err) {
        console.error("Failed to load records:", err);
      }
    }

    function renderTable(data) {
      const thead = document.getElementById("table-head");
      const tbody = document.getElementById("table-body");
      const footerCount = document.getElementById("footer-count");

      footerCount.innerText = `${data.length} of ${data.length}`;

      if (currentDocType === "Department") {
        thead.innerHTML = `
          <tr>
            <th width="40"><input type="checkbox"></th>
            <th>ID</th>
            <th>Status</th>
            <th>Department</th>
            <th>Parent Department</th>
            <th>Is Group</th>
            <th>Leave Block List</th>
            <th width="100" style="text-align:right;"></th>
          </tr>
        `;
        tbody.innerHTML = data.map(row => `
          <tr onclick="openEditRecord('${row.name}')">
            <td><input type="checkbox" onclick="event.stopPropagation()"></td>
            <td class="td-id">${row.name}</td>
            <td><span class="status-badge">Enabled</span></td>
            <td>${row.department_name || row.name}</td>
            <td style="color:#6b7280;">${row.parent_department || ""}</td>
            <td>${row.is_group ? '<span class="check-icon">✔</span>' : '<span style="color:#d1d5db;">◻</span>'}</td>
            <td>-</td>
            <td style="text-align:right;">
              <div class="meta-icons" style="justify-content: flex-end;">
                <span>now</span>
                <span>💬 0</span>
                <span>♡</span>
              </div>
            </td>
          </tr>
        `).join("");
      } else if (currentDocType === "Designation") {
        thead.innerHTML = `
          <tr>
            <th width="40"><input type="checkbox"></th>
            <th>ID</th>
            <th>Status</th>
            <th>Designation Name</th>
            <th>Description</th>
            <th width="100" style="text-align:right;"></th>
          </tr>
        `;
        tbody.innerHTML = data.map(row => `
          <tr onclick="openEditRecord('${row.name}')">
            <td><input type="checkbox" onclick="event.stopPropagation()"></td>
            <td class="td-id">${row.name}</td>
            <td><span class="status-badge">Enabled</span></td>
            <td>${row.designation_name || row.name}</td>
            <td style="color:#6b7280;">${row.description || ""}</td>
            <td style="text-align:right;">
              <div class="meta-icons" style="justify-content: flex-end;">
                <span>now</span>
                <span>💬 0</span>
                <span>♡</span>
              </div>
            </td>
          </tr>
        `).join("");
      } else if (currentDocType === "Employee") {
        thead.innerHTML = `
          <tr>
            <th width="40"><input type="checkbox"></th>
            <th>ID</th>
            <th>Status</th>
            <th>Employee Name</th>
            <th>Department</th>
            <th>Designation</th>
            <th>Company</th>
            <th width="100" style="text-align:right;"></th>
          </tr>
        `;
        tbody.innerHTML = data.map(row => `
          <tr onclick="openEditRecord('${row.name}')">
            <td><input type="checkbox" onclick="event.stopPropagation()"></td>
            <td class="td-id">${row.name}</td>
            <td><span class="status-badge" style="background:#ecfdf5; color:#059669;">Active</span></td>
            <td>${row.employee_name || row.first_name || row.name}</td>
            <td>${row.department || ""}</td>
            <td>${row.designation || ""}</td>
            <td>${row.company || "My Company"}</td>
            <td style="text-align:right;">
              <div class="meta-icons" style="justify-content: flex-end;">
                <span>now</span>
                <span>💬 0</span>
                <span>♡</span>
              </div>
            </td>
          </tr>
        `).join("");
      } else {
        // Generic Table Renderer
        const keys = data.length > 0 ? Object.keys(data[0]).filter(k => !['creation','modified','modified_by','owner','docstatus','idx'].includes(k)).slice(0, 6) : ['name'];
        thead.innerHTML = `
          <tr>
            <th width="40"><input type="checkbox"></th>
            ${keys.map(k => `<th>${k.replace(/_/g, ' ').toUpperCase()}</th>`).join("")}
            <th width="100" style="text-align:right;"></th>
          </tr>
        `;
        tbody.innerHTML = data.map(row => `
          <tr onclick="openEditRecord('${row.name}')">
            <td><input type="checkbox" onclick="event.stopPropagation()"></td>
            ${keys.map(k => `<td>${row[k] !== null && row[k] !== undefined ? row[k] : ''}</td>`).join("")}
            <td style="text-align:right;">
              <div class="meta-icons" style="justify-content: flex-end;">
                <span>now</span>
                <span>💬 0</span>
                <span>♡</span>
              </div>
            </td>
          </tr>
        `).join("");
      }
    }

    function applyClientFilter() {
      const idVal = document.getElementById("filter-id").value.toLowerCase();
      const compVal = document.getElementById("filter-company").value.toLowerCase();
      
      const filtered = recordsData.filter(r => {
        const nameMatch = !idVal || (r.name && r.name.toLowerCase().includes(idVal)) || (r.department_name && r.department_name.toLowerCase().includes(idVal)) || (r.designation_name && r.designation_name.toLowerCase().includes(idVal));
        const compMatch = !compVal || (r.company && r.company.toLowerCase().includes(compVal));
        return nameMatch && compMatch;
      });
      renderTable(filtered);
    }

    // Modal Operations
    function openAddModal() {
      const modal = document.getElementById("add-modal");
      const title = document.getElementById("modal-title");
      const body = document.getElementById("modal-form-fields");

      title.innerText = `New ${currentDocType}`;
      modal.classList.add("open");

      if (currentDocType === "Department") {
        body.innerHTML = `
          <div class="form-group">
            <label class="form-label">Department Name *</label>
            <input type="text" id="f-dept-name" class="form-control" placeholder="e.g. Legal & Compliance">
          </div>
          <div class="form-group">
            <label class="form-label">Parent Department</label>
            <select id="f-dept-parent" class="form-control">
              <option value="All Departments">All Departments</option>
              ${recordsData.map(r => `<option value="${r.name}">${r.name}</option>`).join("")}
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Company</label>
            <input type="text" id="f-dept-company" class="form-control" value="My Company">
          </div>
          <label class="form-check">
            <input type="checkbox" id="f-dept-group">
            Is Group
          </label>
        `;
      } else if (currentDocType === "Designation") {
        body.innerHTML = `
          <div class="form-group">
            <label class="form-label">Designation Name *</label>
            <input type="text" id="f-desig-name" class="form-control" placeholder="e.g. Product Architect">
          </div>
          <div class="form-group">
            <label class="form-label">Description</label>
            <textarea id="f-desig-desc" class="form-control" rows="3" placeholder="Key responsibilities and duties..."></textarea>
          </div>
        `;
      } else if (currentDocType === "Employee") {
        body.innerHTML = `
          <div class="form-group">
            <label class="form-label">First Name *</label>
            <input type="text" id="f-emp-first" class="form-control" placeholder="First Name">
          </div>
          <div class="form-group">
            <label class="form-label">Last Name</label>
            <input type="text" id="f-emp-last" class="form-control" placeholder="Last Name">
          </div>
          <div class="form-group">
            <label class="form-label">Department</label>
            <input type="text" id="f-emp-dept" class="form-control" placeholder="Operations">
          </div>
          <div class="form-group">
            <label class="form-label">Designation</label>
            <input type="text" id="f-emp-desig" class="form-control" placeholder="Software Engineer">
          </div>
          <div class="form-group">
            <label class="form-label">Date of Joining</label>
            <input type="date" id="f-emp-doj" class="form-control" value="${new Date().toISOString().split('T')[0]}">
          </div>
        `;
      } else {
        body.innerHTML = `
          <div class="form-group">
            <label class="form-label">Name *</label>
            <input type="text" id="f-gen-name" class="form-control" placeholder="Name">
          </div>
        `;
      }
    }

    function closeAddModal() {
      document.getElementById("add-modal").classList.remove("open");
    }

    async function submitNewRecord() {
      let doc = { doctype: currentDocType };
      if (currentDocType === "Department") {
        const dName = document.getElementById("f-dept-name").value.trim();
        if (!dName) return alert("Department Name is required");
        doc.department_name = dName;
        doc.name = dName.endsWith("- W") ? dName : `${dName} - W`;
        doc.parent_department = document.getElementById("f-dept-parent").value;
        doc.company = document.getElementById("f-dept-company").value;
        doc.is_group = document.getElementById("f-dept-group").checked ? 1 : 0;
        doc.disabled = 0;
      } else if (currentDocType === "Designation") {
        const dName = document.getElementById("f-desig-name").value.trim();
        if (!dName) return alert("Designation Name is required");
        doc.designation_name = dName;
        doc.name = dName;
        doc.description = document.getElementById("f-desig-desc").value.trim();
      } else if (currentDocType === "Employee") {
        const first = document.getElementById("f-emp-first").value.trim();
        if (!first) return alert("First Name is required");
        const last = document.getElementById("f-emp-last").value.trim();
        doc.first_name = first;
        doc.last_name = last;
        doc.employee_name = `${first} ${last}`.trim();
        doc.name = `HR-EMP-${Math.floor(10000 + Math.random() * 90000)}`;
        doc.department = document.getElementById("f-emp-dept").value.trim();
        doc.designation = document.getElementById("f-emp-desig").value.trim();
        doc.date_of_joining = document.getElementById("f-emp-doj").value;
        doc.status = "Active";
        doc.company = "My Company";
      } else {
        const n = document.getElementById("f-gen-name").value.trim();
        if (!n) return alert("Name is required");
        doc.name = n;
      }

      try {
        const res = await fetch("/api/method/frappe.client.insert", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ doc })
        });
        const resJson = await res.json();
        closeAddModal();
        loadDocTypeData();
      } catch (err) {
        alert("Error saving record: " + err.message);
      }
    }

    function openEditRecord(name) {
      // Row detail view or notification
      console.log("Viewing record:", name);
    }

    window.addEventListener("DOMContentLoaded", initRoute);
  </script>
</body>
</html>
"""
