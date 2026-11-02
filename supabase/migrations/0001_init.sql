-- Wonderful — схема базы (Supabase / Postgres)
-- Выполнить один раз в Supabase → SQL Editor.
-- Этот же запрос приложение показывает на экране подключения.

-- 1. Таблицы
create table if not exists public.areas (
  id uuid primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  name text not null,
  color text not null default 'slate',
  sort int not null default 0,
  updated_at timestamptz not null default now(),
  deleted boolean not null default false
);

create table if not exists public.tasks (
  id uuid primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  title text not null,
  next_action text,
  bucket text not null default 'inbox',
  area_id uuid,
  waiting_on text,
  review_at date,
  note text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  done_at timestamptz,
  deleted boolean not null default false
);

create table if not exists public.reviews (
  id uuid primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  done_at timestamptz not null default now(),
  note text,
  updated_at timestamptz not null default now(),
  deleted boolean not null default false
);

-- 2. Индексы
create index if not exists tasks_user_bucket on public.tasks(user_id, bucket);
create index if not exists tasks_user_updated on public.tasks(user_id, updated_at);

-- 3. RLS: доступ только к своим строкам
alter table public.areas   enable row level security;
alter table public.tasks   enable row level security;
alter table public.reviews enable row level security;

drop policy if exists areas_own on public.areas;
create policy areas_own on public.areas for all to authenticated
  using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists tasks_own on public.tasks;
create policy tasks_own on public.tasks for all to authenticated
  using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists reviews_own on public.reviews;
create policy reviews_own on public.reviews for all to authenticated
  using (user_id = auth.uid()) with check (user_id = auth.uid());

-- 4. Realtime (если таблица уже добавлена — ошибку можно игнорировать)
alter publication supabase_realtime add table public.tasks;
alter publication supabase_realtime add table public.areas;
alter publication supabase_realtime add table public.reviews;
