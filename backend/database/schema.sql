CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE usuarios (
	id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	nombre VARCHAR(150) NOT NULL,
	email VARCHAR(100) NOT NULL,
	contrasena_hash VARCHAR(250) NOT NULL,
	moneda VARCHAR(10) DEFAULT 'MXN',
	fecha_creacion TIMESTAMP DEFAULT NOW() 
);

CREATE TABLE categorias (
	id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	nombre VARCHAR(50) NOT NULL,
	icono VARCHAR(50),
	color VARCHAR(30),
	es_default BOOLEAN DEFAULT FALSE
);

CREATE TABLE cuentas (
	id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
	nombre VARCHAR(50) NOT NULL,
	tipo VARCHAR(50) NOT NULL,
	saldo_inicial FLOAT DEFAULT 0,
	saldo_actual FLOAT DEFAULT 0,
	fecha_creacion TIMESTAMP DEFAULT NOW()
);

CREATE TABLE presupuestos (
	id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
	categoria_id UUID NOT NULL REFERENCES categorias(id) ON DELETE CASCADE,
	monto_limite FLOAT NOT NULL,
	periodo VARCHAR(20) NOT NULL,
	fecha_inicio DATE NOT NULL,
	fecha_fin DATE NOT NULL
);

CREATE TABLE transacciones (
	id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
	cuenta_id UUID NOT NULL REFERENCES cuentas(id) ON DELETE CASCADE,
	categoria_id UUID NOT NULL REFERENCES categorias(id) ON DELETE CASCADE,
	monto FLOAT NOT NULL,
	tipo VARCHAR(50) NOT NULL,
	nota VARCHAR(100),
	fecha DATE NOT NULL,
	fecha_creacion TIMESTAMP DEFAULT NOW()
);

CREATE TABLE alertas_ml (
	id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
	tipo_alerta VARCHAR(50) NOT NULL,
	mensaje TEXT NOT NULL,
	valor_detectado FLOAT,
	leida BOOLEAN DEFAULT FALSE,
	generada_en TIMESTAMP DEFAULT NOW()
);