-- Create the feedback table (run this if you don't have the table yet)
create table if not exists feedback (
  id bigint generated always as identity primary key,
  spot_id int,
  busy_rating int check (busy_rating between 1 and 10),
  accuracy_rating int check (accuracy_rating between 1 and 10),
  comment text,
  client_session_id text,
  created_at timestamptz default now()
);

-- Enable Row Level Security
alter table feedback enable row level security;

-- Allow anonymous inserts only
create policy "allow anon insert"
on feedback
for insert
to anon
with check (true);

-- Prevent anon users from selecting/updating/deleting others' data
create policy "deny select"
on feedback
for select
using (false);

create policy "deny update"
on feedback
for update
using (false);

create policy "deny delete"
on feedback
for delete
using (false);
