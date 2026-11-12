import { useEffect, useState } from 'react';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${API_URL}/tasks`);
      const data = await response.json();
      setTasks(data);
    } catch (err) {
      setError('No se pudo conectar con el backend.');
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!title.trim()) {
      setError('El título es obligatorio.');
      return;
    }

    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, description }),
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || 'No se pudo crear la tarea');
      }

      setTitle('');
      setDescription('');
      setError('');
      await fetchTasks();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (id) => {
    try {
      const response = await fetch(`${API_URL}/tasks/${id}/toggle`, {
        method: 'PATCH',
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || 'No se pudo cambiar el estado');
      }

      setTasks((currentTasks) =>
        currentTasks.map((task) =>
          task.id === payload.id ? { ...task, completed: payload.completed } : task
        )
      );
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`${API_URL}/tasks/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const payload = await response.json();
        throw new Error(payload.error || 'No se pudo eliminar la tarea');
      }

      setTasks((currentTasks) => currentTasks.filter((task) => task.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Sistema de gestión</p>
          <h1>Gestor de Tareas</h1>
        </div>
      </header>

      <main className="content-grid">
        <section className="panel form-panel">
          <h2>Nueva tarea</h2>
          <form onSubmit={handleSubmit} className="task-form">
            <label>
              Título
              <input
                type="text"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="Ej. Revisar backlog"
              />
            </label>

            <label>
              Descripción
              <textarea
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                placeholder="Agregar contexto o próximos pasos"
                rows="4"
              />
            </label>

            {error && <p className="error-message">{error}</p>}

            <button type="submit" disabled={loading}>
              {loading ? 'Guardando...' : 'Guardar tarea'}
            </button>
          </form>
        </section>

        <section className="panel list-panel">
          <h2>Listado</h2>
          <div className="task-list">
            {tasks.length === 0 ? (
              <p className="empty-state">Aún no hay tareas registradas.</p>
            ) : (
              tasks.map((task) => (
                <article key={task.id} className={`task-card ${task.completed ? 'completed' : ''}`}>
                  <div>
                    <h3>{task.title}</h3>
                    <p>{task.description || 'Sin descripción adicional.'}</p>
                    <small>{new Date(task.created_at).toLocaleDateString()}</small>
                  </div>

                  <div className="task-actions">
                    <button
                      className="secondary"
                      onClick={() => handleToggle(task.id)}
                    >
                      {task.completed ? 'Reabrir' : 'Completar'}
                    </button>
                    <button className="danger" onClick={() => handleDelete(task.id)}>
                      Eliminar
                    </button>
                  </div>
                </article>
              ))
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
