import pandas as pd
import os
from django.core.management.base import BaseCommand
from dashboard.models import WorldBankData
import re


class Command(BaseCommand):
    help = 'Seeds the database from the final_data.csv file with a definitive exclusion list.'

    def handle(self, *args, **kwargs):
        NON_COUNTRY_REGIONS = [
            'Africa Eastern and Southern', 'Africa Western and Central', 'Arab World',
            'Caribbean small states', 'Central Europe and the Baltics', 'Early-demographic dividend',
            'East Asia & Pacific', 'East Asia & Pacific (excluding high income)',
            'East Asia & Pacific (IDA & IBRD countries)', 'Euro area', 'Europe & Central Asia',
            'Europe & Central Asia (excluding high income)', 'Europe & Central Asia (IDA & IBRD countries)',
            'European Union', 'Fragile and conflict affected situations',
            'Heavily indebted poor countries (HIPC)', 'High income', 'IBRD only', 'IDA & IBRD total',
            'IDA blend', 'IDA only', 'IDA total', 'Late-demographic dividend',
            'Latin America & Caribbean', 'Latin America & Caribbean (excluding high income)',
            'Latin America & the Caribbean (IDA & IBRD countries)', 'Least developed countries: UN classification',
            'Low & middle income', 'Low income', 'Lower middle income', 'Middle East & North Africa',
            'Middle East & North Africa (excluding high income)', 'Middle East & North Africa (IDA & IBRD countries)',
            'Middle income', 'North America', 'Not classified', 'OECD members', 'Other small states',
            'Pacific island small states', 'Post-demographic dividend', 'Pre-demographic dividend',
            'Small states', 'South Asia', 'South Asia (IDA & IBRD)', 'Sub-Saharan Africa',
            'Sub-Saharan Africa (excluding high income)', 'Sub-Saharan Africa (IDA & IBRD countries)',
            'Upper middle income', 'World'
        ]

        self.stdout.write('Clearing existing data...')
        WorldBankData.objects.all().delete()

        csv_file_path = os.path.join('data', 'data.csv')
        self.stdout.write(f'Processing {csv_file_path}...')

        try:
            df = pd.read_csv(csv_file_path)

            df['Country Name'] = df['Country Name'].str.strip()
            df = df[~df['Country Name'].isin(NON_COUNTRY_REGIONS)]

            def clean_year_columns(col_name):
                match = re.search(r'\d{4}', col_name)
                return match.group(0) if match else col_name
            df.rename(columns=clean_year_columns, inplace=True)

            id_vars = ['Country Name', 'Country Code',
                       'Series Name', 'Series Code']
            df_melted = df.melt(
                id_vars=id_vars, var_name='year', value_name='value')

            df_cleaned = df_melted.dropna(subset=['value'])
            df_cleaned = df_cleaned[df_cleaned['value'] != '..']
            df_cleaned['year'] = pd.to_numeric(df_cleaned['year'])
            df_cleaned['value'] = pd.to_numeric(df_cleaned['value'])

            df_cleaned.rename(columns={
                'Country Name': 'country', 'Country Code': 'country_code', 'Series Name': 'series',
            }, inplace=True)

            final_df = df_cleaned[['country',
                                   'country_code', 'series', 'year', 'value']]

            records = final_df.to_dict('records')
            model_instances = [WorldBankData(**rec) for rec in records]

            self.stdout.write('Importing clean data to the database...')
            WorldBankData.objects.bulk_create(model_instances)

            self.stdout.write(self.style.SUCCESS(
                f'Successfully imported {len(model_instances)} clean records.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
