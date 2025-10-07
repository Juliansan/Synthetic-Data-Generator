#!/usr/bin/env python3
"""
Data Generator CLI
Generate synthetic data from YAML configuration files
"""

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich import box
from pathlib import Path
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config_parser import ConfigParser
from generators import (
    EnvironmentalSensorGenerator,
    BusinessDataGenerator,
    UserDataGenerator,
    LogDataGenerator
)

console = Console()


def create_generator(config: ConfigParser):
    """Create appropriate generator based on config"""
    gen_type = config.get_generator_type()
    seed = config.get_seed()
    
    if gen_type == 'environmental_sensor':
        return EnvironmentalSensorGenerator(seed=seed)
    elif gen_type.startswith('business'):
        return BusinessDataGenerator(seed=seed)
    elif gen_type.startswith('user'):
        return UserDataGenerator(seed=seed)
    elif gen_type == 'job_logs' or gen_type.startswith('log'):
        return LogDataGenerator(seed=seed)
    else:
        raise ValueError(f"Unknown generator type: {gen_type}")


def generate_environmental_sensor(config: ConfigParser):
    """Generate environmental sensor data"""
    generator = EnvironmentalSensorGenerator(seed=config.get_seed())
    settings = config.get_settings()
    
    # Parse settings
    freq = settings.get('frequency', '5min')
    start_date = config.parse_date(settings.get('start_date'))
    
    # Get range settings
    temp_settings = settings.get('temperature', {})
    temp_range = (temp_settings.get('min', 15.0), temp_settings.get('max', 30.0))
    
    humidity_settings = settings.get('humidity', {})
    humidity_range = (humidity_settings.get('min', 30.0), humidity_settings.get('max', 80.0))
    
    co2_settings = settings.get('co2_level', {})
    co2_range = (co2_settings.get('min', 400), co2_settings.get('max', 1200))
    
    # Get sensor configuration
    sensors_config = settings.get('sensors', [])
    sensor_ids = [s['id'] for s in sensors_config] if sensors_config else None
    include_location = bool(sensors_config and any('location' in s for s in sensors_config))
    
    # Get anomaly settings
    anomaly_config = settings.get('anomalies', {})
    add_anomalies = anomaly_config.get('enabled', False)
    anomaly_rate = anomaly_config.get('rate', 0.0)
    
    # Build null configuration
    null_config = {}
    for field in ['temperature', 'humidity', 'co2_level']:
        field_settings = settings.get(field, {})
        if field_settings.get('nullable', False):
            null_config[field] = field_settings.get('null_rate', 0.0)
    
    # Generate data
    df = generator.generate(
        n_rows=config.get_rows(),
        start_date=start_date,
        freq=freq,
        sensor_ids=sensor_ids,
        include_location=include_location,
        temp_range=temp_range,
        humidity_range=humidity_range,
        co2_range=co2_range,
        add_anomalies=add_anomalies,
        anomaly_rate=anomaly_rate,
        null_config=null_config
    )
    
    # Add custom locations if specified
    if include_location and sensors_config:
        location_map = {s['id']: s.get('location', f"Location for {s['id']}") 
                       for s in sensors_config}
        df['location'] = df['sensor_id'].map(location_map)
    
    return df


def generate_business_customers(config: ConfigParser):
    """Generate business customer data"""
    generator = BusinessDataGenerator(seed=config.get_seed())
    settings = config.get_settings()
    
    df = generator.generate_customers(
        n_rows=config.get_rows(),
        include_address=settings.get('include_address', True),
        include_signup_date=settings.get('include_signup_date', True)
    )
    
    # Apply null values
    columns_config = settings.get('columns', {})
    for column, col_settings in columns_config.items():
        if column in df.columns and col_settings.get('nullable', False):
            null_rate = col_settings.get('null_rate', 0.0)
            if null_rate > 0:
                df[column] = generator.add_nulls(df[column], null_rate)
    
    return df


def generate_business_transactions(config: ConfigParser):
    """Generate business transaction data"""
    generator = BusinessDataGenerator(seed=config.get_seed())
    settings = config.get_settings()
    
    df = generator.generate_transactions(
        n_rows=config.get_rows(),
        n_customers=settings.get('n_customers', config.get_rows() // 3),
        start_date=config.parse_date(settings.get('start_date')),
        end_date=config.parse_date(settings.get('end_date')),
        include_shipping=settings.get('include_shipping', True)
    )
    
    # Apply null values
    columns_config = settings.get('columns', {})
    for column, col_settings in columns_config.items():
        if column in df.columns and col_settings.get('nullable', False):
            null_rate = col_settings.get('null_rate', 0.0)
            if null_rate > 0:
                df[column] = generator.add_nulls(df[column], null_rate)
    
    return df


def generate_user_profiles(config: ConfigParser):
    """Generate user profile data"""
    generator = UserDataGenerator(seed=config.get_seed())
    settings = config.get_settings()
    
    df = generator.generate_user_profiles(
        n_rows=config.get_rows(),
        include_bio=settings.get('include_bio', False),
        include_social=settings.get('include_social', False)
    )
    
    # Apply null values
    columns_config = settings.get('columns', {})
    for column, col_settings in columns_config.items():
        if column in df.columns and col_settings.get('nullable', False):
            null_rate = col_settings.get('null_rate', 0.0)
            if null_rate > 0:
                df[column] = generator.add_nulls(df[column], null_rate)
    
    return df


def generate_job_logs(config: ConfigParser):
    """Generate job/process log data"""
    generator = LogDataGenerator(seed=config.get_seed())
    settings = config.get_settings()
    
    # Get time range
    start_date = config.parse_date(settings.get('start_date'))
    end_date = config.parse_date(settings.get('end_date'))
    
    # Get frequency
    freq = settings.get('frequency', '15min')
    
    # Get custom job names if provided
    job_names = settings.get('job_names', None)
    
    # Get status distribution
    status_dist = settings.get('status_distribution', None)
    
    # Get duration range
    duration_config = settings.get('duration', {})
    duration_range = (
        duration_config.get('min', 10),
        duration_config.get('max', 300)
    )
    
    # Additional fields
    include_error_message = settings.get('include_error_message', False)
    include_severity = settings.get('include_severity', False)
    
    # Generate data
    df = generator.generate(
        n_rows=config.get_rows(),
        start_date=start_date,
        end_date=end_date,
        freq=freq,
        job_names=job_names,
        status_distribution=status_dist,
        duration_range=duration_range,
        include_error_message=include_error_message,
        include_severity=include_severity
    )
    
    return df


@click.group()
@click.version_option(version="2.0.0")
def cli():
    """
    🎨 Data Generator CLI
    
    Generate realistic synthetic data from YAML configuration files.
    """
    pass


@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--preview', '-p', default=5, help='Number of rows to preview (0 to disable)')
@click.option('--stats', '-s', is_flag=True, help='Show statistics about generated data')
def generate(config_file, preview, stats):
    """Generate data from a YAML configuration file"""
    
    try:
        # Load configuration
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Loading configuration...", total=None)
            config = ConfigParser(config_file)
            progress.update(task, completed=True)
        
        # Display configuration
        console.print()
        console.print(Panel.fit(
            f"[bold cyan]Generator:[/bold cyan] {config.get_generator_type()}\n"
            f"[bold cyan]Rows:[/bold cyan] {config.get_rows():,}\n"
            f"[bold cyan]Output:[/bold cyan] {config.get_output_file()}\n"
            f"[bold cyan]Seed:[/bold cyan] {config.get_seed() or 'Random'}",
            title="[bold green]Configuration[/bold green]",
            border_style="green"
        ))
        
        # Generate data
        console.print()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(
                f"Generating {config.get_rows():,} rows...", 
                total=None
            )
            
            gen_type = config.get_generator_type()
            
            if gen_type == 'environmental_sensor':
                df = generate_environmental_sensor(config)
            elif gen_type == 'business_customers':
                df = generate_business_customers(config)
            elif gen_type == 'business_transactions':
                df = generate_business_transactions(config)
            elif gen_type == 'user_profiles':
                df = generate_user_profiles(config)
            elif gen_type == 'job_logs' or gen_type.startswith('log'):
                df = generate_job_logs(config)
            else:
                raise ValueError(f"Generator type not implemented: {gen_type}")
            
            progress.update(task, completed=True)
        
        # Save data
        output_file = Path(config.get_output_file())
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Saving data...", total=None)
            df.to_csv(output_file, index=False)
            progress.update(task, completed=True)
        
        # Success message
        console.print()
        console.print(f"[bold green]✓[/bold green] Generated {len(df):,} rows")
        console.print(f"[bold green]✓[/bold green] Saved to [cyan]{output_file}[/cyan]")
        
        # Preview
        if preview > 0:
            console.print()
            console.print(Panel.fit(
                f"[bold]Preview (first {min(preview, len(df))} rows)[/bold]",
                border_style="blue"
            ))
            
            table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
            for column in df.columns:
                table.add_column(column, style="cyan")
            
            for idx, row in df.head(preview).iterrows():
                table.add_row(*[str(val) for val in row])
            
            console.print(table)
        
        # Statistics
        if stats:
            console.print()
            console.print(Panel.fit(
                "[bold]Data Statistics[/bold]",
                border_style="blue"
            ))
            
            # Numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                stats_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
                stats_table.add_column("Column", style="cyan")
                stats_table.add_column("Mean", justify="right")
                stats_table.add_column("Min", justify="right")
                stats_table.add_column("Max", justify="right")
                stats_table.add_column("Nulls", justify="right")
                
                for col in numeric_cols:
                    null_count = df[col].isna().sum()
                    null_pct = (null_count / len(df) * 100) if len(df) > 0 else 0
                    stats_table.add_row(
                        col,
                        f"{df[col].mean():.2f}",
                        f"{df[col].min():.2f}",
                        f"{df[col].max():.2f}",
                        f"{null_count} ({null_pct:.1f}%)"
                    )
                
                console.print(stats_table)
        
        console.print()
        
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


@cli.command()
def list_configs():
    """List available configuration files"""
    config_dir = Path('config')
    
    if not config_dir.exists():
        console.print("[yellow]No config directory found[/yellow]")
        return
    
    configs = list(config_dir.glob('*.yaml')) + list(config_dir.glob('*.yml'))
    
    if not configs:
        console.print("[yellow]No configuration files found in config/[/yellow]")
        return
    
    console.print()
    console.print(Panel.fit(
        "[bold]Available Configuration Files[/bold]",
        border_style="green"
    ))
    
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("File", style="cyan")
    table.add_column("Generator Type", style="green")
    table.add_column("Rows")
    
    for config_file in sorted(configs):
        try:
            config = ConfigParser(str(config_file))
            table.add_row(
                config_file.name,
                config.get_generator_type(),
                f"{config.get_rows():,}"
            )
        except Exception as e:
            table.add_row(config_file.name, "[red]Error[/red]", str(e))
    
    console.print(table)
    console.print()


@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
def validate(config_file):
    """Validate a YAML configuration file"""
    try:
        config = ConfigParser(config_file)
        
        console.print()
        console.print("[bold green]✓[/bold green] Configuration is valid!")
        console.print()
        console.print(Panel.fit(
            f"[bold cyan]Generator:[/bold cyan] {config.get_generator_type()}\n"
            f"[bold cyan]Rows:[/bold cyan] {config.get_rows():,}\n"
            f"[bold cyan]Output:[/bold cyan] {config.get_output_file()}\n"
            f"[bold cyan]Seed:[/bold cyan] {config.get_seed() or 'Random'}",
            title="[bold green]Configuration Details[/bold green]",
            border_style="green"
        ))
        console.print()
        
    except Exception as e:
        console.print(f"\n[bold red]✗[/bold red] Validation failed:")
        console.print(f"  {str(e)}\n")
        sys.exit(1)


if __name__ == '__main__':
    cli()
