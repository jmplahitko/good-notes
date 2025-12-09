# Desktop Note-Taking App - Final Implementation Plan

## Architecture Overview

Transform the existing Nuxt starter template into an Electron desktop application with:
- Electron wrapper for desktop functionality
- Python backend (FastAPI) running as subprocess managed by Electron
- VS Code default dark theme
- File system storage: notes as markdown files (converted from JSON), action items in single JSON file
- Elasticsearch for note search (Python backend)
- Rich text editor (simple WYSIWYG) in Nuxt frontend
- Strict frontend architecture with reactive stores and clear data flow

## Data Flow Architecture

1. **Pages/Components** → Call store actions (e.g., `notesStore.createNote(data)`)
2. **Stores** → Send data to backend API
3. **Backend** → Apply business rules, save to file system, return updated data
4. **Stores** → Overwrite cache with backend response (reactive state)
5. **Pages/Components** → Automatically react to store state changes via Vue reactivity

## Key Files to Create/Modify

### Python Backend
- `backend/main.py` - FastAPI application entry point
- `backend/api/notes.py` - Note CRUD endpoints (receive JSON, convert to markdown, return JSON)
- `backend/api/action_items.py` - Action item CRUD endpoints (single JSON file)
- `backend/api/search.py` - Elasticsearch search endpoint
- `backend/services/file_system.py` - File system operations
- `backend/services/notes_manager.py` - Note CRUD: JSON -> Markdown conversion (title->h1, attendees->optional "Attendees" h2 section, content->markdown, metadata->frontmatter)
- `backend/services/action_items_manager.py` - Action item CRUD (single JSON file storage)
- `backend/services/settings_manager.py` - Settings CRUD (JSON format)
- `backend/services/markdown_converter.py` - Convert note JSON to markdown and parse markdown back to JSON
- `backend/services/file_naming.py` - Generate filenames from note title and meeting start time (slugify + time formatting)
- `backend/services/elasticsearch_service.py` - Elasticsearch client setup and indexing
- `backend/models/note.py` - Note Pydantic models (JSON format)
- `backend/models/action_item.py` - ActionItem Pydantic models (JSON format)
- `backend/config.py` - Configuration (notes directory, action items JSON path, Elasticsearch settings, API port)
- `backend/requirements.txt` - Python dependencies
- `backend/__init__.py` - Python package initialization

### Electron Setup
- `electron/main.js` - Main Electron process (window management, Python backend process management)
- `electron/preload.js` - Preload script for secure IPC communication
- Update `package.json` - Add Electron dependencies and build scripts

### Frontend Stores (Composables - Data Management)
- `app/composables/stores/useApi.ts` - Base API client for Python backend communication
- `app/composables/stores/useNotesStore.ts` - Notes store:
  - Reactive state: `const notes = ref<Note[]>([])`, `const currentNote = ref<Note | null>(null)`
  - Actions: `createNote(data)`, `updateNote(id, data)`, `deleteNote(id)`, `fetchNotes()`, `fetchNoteById(id)`
  - Actions send data to backend, backend returns updated state, store overwrites cache
  - Pages/components reactively update when store state changes
- `app/composables/stores/useActionItemsStore.ts` - Action items store:
  - Reactive state: `const actionItems = ref<ActionItem[]>([])`, `const currentActionItem = ref<ActionItem | null>(null)`
  - Actions: `createActionItem(data)`, `updateActionItem(id, data)`, `completeActionItem(id)`, `fetchActionItems()`, `fetchActionItemById(id)`
  - Same pattern: send to backend, receive updated state, overwrite cache
- `app/composables/stores/useSearchStore.ts` - Search store (cache and fetch search results)
- `app/composables/stores/useSettingsStore.ts` - Settings store:
  - Reactive state: `const settings = ref<Settings | null>(null)`
  - Actions: `updateSettings(data)`, `fetchSettings()`
  - Same pattern: send to backend, receive updated state, overwrite cache

### Middleware (Data Orchestration)
- `app/middleware/home.ts` - Fetch oldest 5 incomplete action items, today's notes, yesterday's notes
- `app/middleware/notes.ts` - Fetch notes list or search results
- `app/middleware/note-detail.ts` - Fetch single note by ID
- `app/middleware/action-items.ts` - Fetch action items list or search results
- `app/middleware/action-item-detail.ts` - Fetch single action item by ID
- `app/middleware/settings.ts` - Fetch settings data

### Pages (Presentation Only)
- `app/pages/index.vue` - Home page (create note, oldest 5 incomplete action items, today's notes, yesterday's notes)
- `app/pages/notes/index.vue` - Notes list page with search
- `app/pages/notes/[id].vue` - View/Update a note
- `app/pages/notes/create.vue` - Create note page
- `app/pages/action-items/index.vue` - Action items list page with search
- `app/pages/action-items/[id].vue` - View/Update/Complete action item
- `app/pages/settings.vue` - Settings page (storage location, Elasticsearch configuration)

### UI Components (Presentation Only)
- `app/components/NoteList.vue` - Note list component (receives data via props, emits events)
- `app/components/NoteCard.vue` - Note card for display
- `app/components/ActionItemList.vue` - Action items list component
- `app/components/ActionItemCard.vue` - Action item card for display
- `app/components/SearchBar.vue` - Search interface (emits search events)
- `app/components/CreateNoteForm.vue` - Create note form (emits submit events, includes attendees input field)
- `app/components/NoteEditor.vue` - Note editor component (emits save events)
- `app/components/AttendeesInput.vue` - Attendees input component (plain text list input, emits update events)
- `app/components/ActionItemForm.vue` - Action item form (emits submit events)
- `app/components/SettingsForm.vue` - Settings form (emits submit events)

### Rich Text Editor
- `app/components/NoteEditor.vue` - Rich text editor component (TipTap)
- `app/composables/useNoteEditor.ts` - Editor state management (presentation only)

### Theme & Styling
- `app/assets/css/vscode-theme.css` - VS Code default dark theme color definitions
- Update `app/app.config.ts` - Configure Nuxt UI theme with VS Code colors
- Update `app/assets/css/main.css` - Import VS Code theme and apply styles

### Models & Types
- Update `model/Note.ts` - Add optional `attendees?: string[]` and `meetingStartTime?: Date` fields, ensure compatibility with JSON API and markdown storage
- Update `model/ActionItem.ts` - Ensure compatibility with JSON API
- `model/SearchResult.ts` - Search result types

### Configuration
- Update `nuxt.config.ts` - Configure for Electron (disable SSR, set API base URL)
- `.electron-builder.yml` - Electron Builder configuration (include Python backend)
- Update `package.json` - Add scripts for Python backend management

## Implementation Steps

1. **VS Code Theme Integration**
   - Create VS Code default dark theme color palette
   - Configure Nuxt UI theme system with VS Code colors
   - Set dark theme as default
   - Apply theme to all UI components

2. **Python Backend Setup**
   - Create Python backend structure with FastAPI
   - Set up virtual environment and requirements.txt
   - Create main FastAPI app with CORS configuration for Electron
   - Implement markdown converter service:
     - Convert note JSON to markdown: title -> h1 heading, attendees -> optional "Attendees" h2 section (if present, placed after title and before content), content -> markdown format
     - Add file metadata (id, dates, meetingStartTime if present, etc.) to frontmatter
     - Parse markdown files back to JSON (extract frontmatter including meetingStartTime, parse "Attendees" h2 section if present, convert markdown to content)
   - Create notes directory structure: `~/Documents/GoodNotes/notes/YYYYMMDD/` (subdirectories by day based on createdAt date)
   - Implement file naming: slugified title + optional meeting start time (HHMM format) + `.md` extension
   - Handle pending note state: notes exist in memory/UI before save, createdAt is set when note is first saved
   - Set up action items JSON file storage (single file for all action items)

3. **Elasticsearch Integration (Python)**
   - Install and configure Elasticsearch Python client
   - Create index mappings for notes (from markdown files) and action items (from YAML file)
   - Implement indexing on note create/update (index markdown content)
   - Implement indexing on action item create/update (index from YAML file)
   - Create search endpoint with query building
   - **Search Strategy**: The frontend `notesStore.search(query?)` action currently fetches all notes from `GET /api/notes` and filters locally. When Elasticsearch is ready:
     1. Update `GET /api/notes` to accept an optional `?q=` query parameter
     2. Backend checks if Elasticsearch is enabled in settings
     3. If ES enabled and query provided: use Elasticsearch to search and return matching notes
     4. If ES disabled or no query: return all notes (current behavior)
     5. Frontend code remains unchanged - it just passes the query to the same `search()` action

4. **Python API Endpoints**
   - Implement note CRUD endpoints (GET, POST, PUT, DELETE):
     - Receive note JSON data (including optional attendees array and meetingStartTime)
     - Set createdAt timestamp when note is first saved (POST), update updatedAt on modifications (PUT)
     - Generate filename: slugified title + optional meeting start time (HHMM format) + `.md`
     - Create/use directory structure: `notes/YYYYMMDD/` based on createdAt date
     - Convert to markdown format (title -> h1, attendees -> optional "Attendees" h2 section, content -> markdown, metadata -> frontmatter)
     - Write/read .md files in appropriate date directory
     - Return note JSON data (including parsed attendees and meetingStartTime if present in markdown)
   - Implement action item CRUD endpoints:
     - Read/write from single JSON file
     - Handle concurrent updates safely
   - Implement search endpoint with Elasticsearch
   - Add error handling and validation using Pydantic models

5. **Electron Setup**
   - Install electron, electron-builder dependencies
   - Create main process with window management
   - Implement Python backend process spawning and management
   - Handle Python backend lifecycle (start/stop with Electron)
   - Set up HTTP communication between renderer and Python backend
   - Configure API base URL for frontend

6. **Frontend Store Composables**
   - Create store composables with reactive state (ref/reactive):
     - `useNotesStore`: 
       - Reactive state: `notes`, `currentNote`, `pendingNotes` (unsaved notes in memory), `loading`, `error`
       - Actions: `createNote(data)` (sets createdAt on backend), `updateNote(id, data)`, `deleteNote(id)`, `fetchNotes()`, `fetchNoteById(id)`
       - Actions send data to backend, backend returns updated state (with createdAt/updatedAt timestamps), store overwrites cache
       - Pending notes exist in memory until saved, then moved to main notes array
     - `useActionItemsStore`: Same pattern with action items
     - `useSearchStore`: Cache search results
     - `useSettingsStore`: Cache settings with update action
   - All stores use Vue reactivity for automatic UI updates
   - Handle API errors and loading states in stores
   - Configure API base URL (localhost with Python backend port)

7. **Nuxt Middleware for Data Orchestration**
   - Create middleware to orchestrate data fetching:
     - `home.ts`: Fetch oldest 5 incomplete action items, today's notes, yesterday's notes
     - `notes.ts`: Fetch notes list or search results based on route query
     - `note-detail.ts`: Fetch note by ID from route params
     - `action-items.ts`: Fetch action items list or search results based on route query
     - `action-item-detail.ts`: Fetch action item by ID from route params
     - `settings.ts`: Fetch settings data
   - Middleware calls store fetch actions, populates stores before page loads

8. **Rich Text Editor**
   - Choose and integrate rich text editor library (TipTap recommended)
   - Implement markdown import/export
   - Add formatting toolbar (bold, italic, headings, lists)
   - Create NoteEditor component (presentation only, emits save events)

9. **Page Components (Presentation Layer)**
   - Home page (`index.vue`): 
     - Consume reactive data from stores (populated by middleware)
     - Call store actions: `notesStore.createNote()` from form submit
     - Automatically react to store state changes
   - Notes index page (`notes/index.vue`): Search bar, notes list with filtering
   - Note detail page (`notes/[id].vue`): 
     - Consume `currentNote` from store
     - Call `notesStore.updateNote()` on save
   - Create note page (`notes/create.vue`): 
     - Manage pending note state (note exists in memory before save)
     - Call `notesStore.createNote()` on submit (sets createdAt timestamp on backend)
     - Handle pending note updates before save
   - Action items index page (`action-items/index.vue`): Search bar, action items list
   - Action item detail page (`action-items/[id].vue`): 
     - Call `actionItemsStore.updateActionItem()` or `completeActionItem()` on save
   - Settings page (`settings.vue`): Call `settingsStore.updateSettings()` on submit
   - All pages consume reactive data from stores, call store actions for mutations

10. **UI Components (Presentation Only)**
    - Create reusable presentation components:
      - NoteList, NoteCard for displaying notes
      - ActionItemList, ActionItemCard for displaying action items
      - SearchBar, CreateNoteForm, NoteEditor, AttendeesInput, ActionItemForm, SettingsForm
    - Components receive data via props (from stores)
    - Components emit events for user actions (e.g., `@submit`, `@save`, `@delete`)
    - Parent pages handle events by calling store actions
    - Components reactively update when props change (store state changes)
    - No direct API calls or data modification in components

11. **App Layout & Navigation**
    - Replace starter template with note-taking layout
    - Add navigation menu (Home, Notes, Action Items, Settings)
    - Update app header/footer for note-taking context
    - Apply VS Code dark theme throughout

12. **Electron Packaging**
    - Configure Electron Builder to include Python backend
    - Bundle Python runtime or use PyInstaller for standalone executable
    - Set up build scripts for cross-platform distribution
    - Handle Python backend startup in packaged app

13. **Integration & Testing**
    - Wire up all components following architectural rules
    - Test data flow: pages → store actions → backend → store update → page reactivity
    - Test Python backend API endpoints independently
    - Test JSON to markdown conversion and parsing
    - Test file system operations (markdown notes, JSON action items)
    - Test Elasticsearch indexing and search
    - Test Electron app with Python backend integration
    - Test Electron packaging and distribution

## Page Structure

- **Home Page** (`/`)
  - Create a Note
  - Oldest 5 incomplete action items
  - Today's Notes
  - Yesterday's Notes

- **Notes** (`/notes`)
  - Search Notes
  - Sub pages:
    - Notes [id] (`/notes/[id]`) - View/Update a Note
    - Create Note (`/notes/create`)

- **Action Items** (`/action-items`)
  - Search Action Items
  - Sub pages:
    - Action Item [id] (`/action-items/[id]`) - View/Update/Complete action item

- **Settings** (`/settings`)
  - Set storage location
  - Elastic Search configuration

## Architectural Rules

### Frontend Architecture
- **Pages and components**: Only for presentation and collection of data. No fetch orchestration or direct access to HTTP.
- **Stores are composables**: Responsible for caching data locally and fetching from the backend. Data is only fetched and stored. It is never modified directly. Trust the backend to update data and return it.
- **Backend**: Fetches and saves data to the file system. Notes and action items in markdown, settings and file indexes (for referencing entities) in JSON format.
- **Nuxt middlewares**: Used to orchestrate the data fetching and setting for pages.

### Data Flow
1. Pages/Components → Call store actions (e.g., `notesStore.createNote(data)`)
2. Stores → Send data to backend API
3. Backend → Apply business rules, save to file system, return updated data
4. Stores → Overwrite cache with backend response (reactive state)
5. Pages/Components → Automatically react to store state changes via Vue reactivity

### Storage Format
- **Notes**: Saved as markdown files (.md) in date-organized directories
  - Directory structure: `~/Documents/GoodNotes/notes/YYYYMMDD/` (based on createdAt date)
  - Filename: slugified title + optional meeting start time (HHMM format) + `.md` extension
  - `note.title` → h1 heading
  - `note.attendees` → optional "Attendees" h2 section (if present, placed after title and before content)
  - `note.content` → converted to markdown format
  - File metadata added to .md file using frontmatter
  - Notes exist in pending state (memory/UI) before first save, createdAt is set when note is saved
- **Action Items**: Saved in `~/Documents/GoodNotes/action_items.yaml`
- **Settings**: Saved in `~/Documents/GoodNotes/settings.yaml`
- **Notes Index**: Saved in `~/Documents/GoodNotes/notes_index.yaml` (ID → file path mapping for fast lookup without scanning all files)

