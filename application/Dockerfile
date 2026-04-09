# ─── STAGE 1: BUILD ───────────────────────────────────────────
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

# Copy central package management files first
COPY Directory.Packages.props .
COPY global.json .

# Copy project files (better layer caching)
COPY src/Web/Web.csproj                         src/Web/
COPY src/PublicApi/PublicApi.csproj             src/PublicApi/
COPY src/ApplicationCore/ApplicationCore.csproj src/ApplicationCore/
COPY src/Infrastructure/Infrastructure.csproj   src/Infrastructure/
COPY src/BlazorAdmin/BlazorAdmin.csproj         src/BlazorAdmin/
COPY src/BlazorShared/BlazorShared.csproj       src/BlazorShared/

# Restore Web project (pulls all dependencies)
RUN dotnet restore src/Web/Web.csproj

# Copy remaining source code
COPY src/ src/

# Build and publish
RUN dotnet publish src/Web/Web.csproj \
    --configuration Release \
    --no-restore \
    --output /app/publish

# ─── STAGE 2: RUNTIME ─────────────────────────────────────────
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app

# Security: create non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Copy published output from build stage
COPY --from=build /app/publish .

# Set ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Set environment
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Development

ENTRYPOINT ["dotnet", "Web.dll"]