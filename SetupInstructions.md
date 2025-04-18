# Removing unwanted files and make project transfer ready
- Backend
1. remove .venv
2. Remove __pycache__ from all the folders

- Frontend
1. Remove .next
2. Remove node_modules

Remove logs folder

# Important Step
1. Install docker and the command for redis
docker run --name redis-container -p 6379:6379 -d redis
2. Install UV package manager [https://docs.astral.sh/uv/getting-started/installation/]
3. Install pnpm [https://pnpm.io/installation]
- Backend
1. uv venv
2. uv sync
3. Reload the window see if import errors are gone
- Frontend
1. pnpm i
2. pnpm dlx prisma generate [https://github.com/prisma/prisma/issues/7234]
3. pnpm dev