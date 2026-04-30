#!/usr/bin/env python3
"""Extract job postings from HTML and create JSON skill profiles

Moved to scripts/data_processing/ for clearer separation of concerns.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

def extract_job_posting(html_file):
	"""Extract structured content from HTML job posting"""
	with open(html_file, 'r', encoding='utf-8') as f:
		soup = BeautifulSoup(f.read(), 'html.parser')

	output = {}

	# ── Job title ──────────────────────────────────────────────────────────────
	title_tag = soup.find('span', property='title')
	output['job_title'] = title_tag.get_text(strip=True) if title_tag else ""

	# ── Employer ───────────────────────────────────────────────────────────────
	employer_tag = soup.find('span', property='name')
	output['employer'] = employer_tag.get_text(strip=True) if employer_tag else ""

	# ── Location ───────────────────────────────────────────────────────────────
	location_tag = soup.find('span', property='address')
	output['location'] = location_tag.get_text(strip=True) if location_tag else ""

	# ── Salary ─────────────────────────────────────────────────────────────────
	salary_tag = soup.find('span', property='value')
	output['salary'] = salary_tag.get_text(strip=True) if salary_tag else ""

	# ── Employment type ────────────────────────────────────────────────────────
	employment_tag = soup.find('span', property='employmentType')
	output['employment_type'] = employment_tag.get_text(strip=True) if employment_tag else ""

	# ── Main details block (comparisonchart) ───────────────────────────────────
	overview = {}
	chart = soup.find('div', id='comparisonchart')
	if chart:
		# Languages
		lang_h4 = chart.find('h4', string='Languages')
		if lang_h4:
			lang_p = lang_h4.find_next_sibling('p')
			if lang_p:
				overview['languages'] = lang_p.get_text(strip=True)

		# Education
		edu_list = []
		edu_h4 = chart.find('h4', string='Education')
		if edu_h4:
			edu_ul = edu_h4.find_next_sibling('ul')
			if edu_ul:
				for li in edu_ul.find_all('li'):
					text_spans = li.find_all('span', class_=lambda c: c != 'wb-inv' if c else True)
					text = next((s.get_text(strip=True) for s in text_spans
								 if s.get_text(strip=True) and 'fa-' not in (s.get('class') or [''])[0]), "")
					if text:
						edu_list.append(text)
		if edu_list:
			overview['education'] = edu_list

		# Experience
		exp_h4 = chart.find('h4', string='Experience')
		if exp_h4:
			exp_p = exp_h4.find_next_sibling('p')
			if exp_p:
				text_spans = exp_p.find_all('span')
				text = next((s.get_text(strip=True) for s in text_spans
							 if s.get_text(strip=True) and 'wb-inv' not in (s.get('class') or [])
							 and not any('fa-' in c for c in (s.get('class') or []))), "")
				if text:
					overview['experience'] = text

		# Work setting
		ws_div = chart.find('div', id='jobOverview-1')
		if ws_div:
			setting_list = []
			ul = ws_div.find('ul')
			if ul:
				for li in ul.find_all('li'):
					text = li.get_text(strip=True)
					if text:
						setting_list.append(text)
			if setting_list:
				overview['work_setting'] = setting_list

	output['overview'] = overview

	# ── Responsibilities ───────────────────────────────────────────────────────
	responsibilities = {}
	resp_div = soup.find('div', id='jobOverview-2')
	if resp_div:
		for h4 in resp_div.find_all('h4'):
			category = h4.get_text(strip=True)
			items = []
			ul = h4.find_next_sibling('ul')
			if ul:
				for li in ul.find_all('li'):
					text = li.find_all('span')[-1].get_text(strip=True) if li.find_all('span') else li.get_text(strip=True)
					if text:
						items.append(text)
			if items:
				responsibilities[category] = items
	if responsibilities:
		output['responsibilities'] = responsibilities

	# ── Experience and specialization ──────────────────────────────────────────
	specialization = {}
	exp_div = soup.find('div', id='jobOverview-4')
	if exp_div:
		for h4 in exp_div.find_all('h4'):
			category = h4.get_text(strip=True)
			items = []
			ul = h4.find_next_sibling('ul')
			if ul:
				for li in ul.find_all('li'):
					text = li.find_all('span')[-1].get_text(strip=True) if li.find_all('span') else li.get_text(strip=True)
					if text:
						items.append(text)
			if items:
				specialization[category] = items
	if specialization:
		output['specialization'] = specialization

	# ── Additional information ─────────────────────────────────────────────────
	additional = {}
	add_div = soup.find('div', id='jobOverview-5')
	if add_div:
		for h4 in add_div.find_all('h4'):
			category = h4.get_text(strip=True)
			items = []
			ul = h4.find_next_sibling('ul')
			if ul:
				for li in ul.find_all('li'):
					text = li.find_all('span')[-1].get_text(strip=True) if li.find_all('span') else li.get_text(strip=True)
					if text:
						items.append(text)
			if items:
				additional[category] = items
	if additional:
		output['additional'] = additional

	# ── Benefits ───────────────────────────────────────────────────────────────
	benefits = {}
	ben_div = soup.find('div', id='jobOverview-7')
	if ben_div:
		for h4 in ben_div.find_all('h4'):
			category = h4.get_text(strip=True)
			items = []
			ul = h4.find_next_sibling('ul')
			if ul:
				for li in ul.find_all('li'):
					text = li.get_text(strip=True)
					if text:
						items.append(text)
			if items:
				benefits[category] = items
	if benefits:
		output['benefits'] = benefits

	return output


def extract_skills_from_job(job_data, known_facets, facet_names):
	"""Extract skill and facet requirements from job posting"""
    
	# Combine all text from job posting
	all_text = json.dumps(job_data).lower()
    
	# Find known facets
	matched_facets = {}
	for facet_name, facet_id in facet_names.items():
		if facet_name in all_text:
			matched_facets[facet_id] = {
				"facet_name": known_facets[facet_id]['facet_name'],
				"facet_type": known_facets[facet_id]['facet_type'],
				"skill_group": known_facets[facet_id]['skill_group'],
				"required": True,
				"context": "Found in job posting"
			}
    
	# Additional skills not in our database
	additional_skills = {}
	additional_patterns = {
		'java': {'name': 'Java', 'type': 'hands_on_language'},
		'c#': {'name': 'C#', 'type': 'hands_on_language'},
		'kotlin': {'name': 'Kotlin', 'type': 'hands_on_language'},
		'rust': {'name': 'Rust', 'type': 'hands_on_language'},
		'go': {'name': 'Go', 'type': 'hands_on_language'},
		'spring': {'name': 'Spring Framework', 'type': 'hands_on_framework'},
		'asp.net': {'name': 'ASP.NET', 'type': 'hands_on_framework'},
		'microservices': {'name': 'Microservices', 'type': 'strategic_domain'},
		'rest api': {'name': 'REST API', 'type': 'hands_on_tool'},
		'soap': {'name': 'SOAP', 'type': 'hands_on_tool'},
		'grpc': {'name': 'gRPC', 'type': 'hands_on_tool'},
		'sql server': {'name': 'SQL Server', 'type': 'hands_on_platform'},
		'postgresql': {'name': 'PostgreSQL', 'type': 'hands_on_platform'},
		'mongodb': {'name': 'MongoDB', 'type': 'hands_on_platform'},
		'cassandra': {'name': 'Cassandra', 'type': 'hands_on_platform'},
		'elasticsearch': {'name': 'Elasticsearch', 'type': 'hands_on_platform'},
		'jenkins': {'name': 'Jenkins', 'type': 'hands_on_tool'},
		'azure': {'name': 'Azure', 'type': 'hands_on_platform'},
		'gcp': {'name': 'Google Cloud Platform', 'type': 'hands_on_platform'},
		'terraform': {'name': 'Terraform', 'type': 'hands_on_tool'},
		'ansible': {'name': 'Ansible', 'type': 'hands_on_tool'},
		'sonarqube': {'name': 'SonarQube', 'type': 'hands_on_tool'},
		'junit': {'name': 'JUnit', 'type': 'hands_on_tool'},
		'testng': {'name': 'TestNG', 'type': 'hands_on_tool'},
	}
    
	for skill_key, skill_info in additional_patterns.items():
		if skill_key in all_text:
			additional_skills[skill_key] = {
				"facet_name": skill_info['name'],
				"facet_type": skill_info['type'],
				"required": True,
				"context": "Found in job posting (not in skills-index.json)"
			}
    
	return {
		'matched_facets': matched_facets,
		'additional_skills': additional_skills
	}
 

def main():
	# Load skills-index.json
	skills_index_path = '/Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/resume-machine/skills-index.json'
	with open(skills_index_path, 'r') as f:
		skills_index = json.load(f)
    
	# Build facet dictionaries
	known_facets = {}
	for catalog_entry in skills_index['facet_catalog']:
		facet_id = catalog_entry['facet_id'].replace('facet.', '')
		known_facets[facet_id] = catalog_entry
    
	# Create inverted map for fuzzy matching
	facet_names = {}
	for entry in skills_index['facet_catalog']:
		name_lower = entry['facet_name'].lower()
		facet_names[name_lower] = entry['facet_id'].replace('facet.', '')
    
	# Get all HTML files
	job_dir = Path('/Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/jobbankjobs/2026/04/05')
	html_files = sorted(job_dir.glob('*.html'))
    
	print(f"Processing {len(html_files)} job postings...")
	print(f"Known facets: {len(known_facets)}\n")
    
	for html_file in html_files:
		print(f"→ {html_file.name}")
        
		# Extract job posting
		job_data = extract_job_posting(html_file)
        
		# Extract skills
		skills = extract_skills_from_job(job_data, known_facets, facet_names)
        
		# Create JSON output
		output = {
			"$schema": "../../../resume-machine/skills-schema.json",
			"metadata": {
				"source": "Job Bank Canada",
				"extracted_date": datetime.now().isoformat() + "Z",
				"job_title": job_data.get('job_title', ''),
				"employer": job_data.get('employer', ''),
				"location": job_data.get('location', ''),
			},
			"job_posting": job_data,
			"required_skills": skills['matched_facets'],
			"additional_skills": skills['additional_skills'],
			"summary": {
				"matched_facets": len(skills['matched_facets']),
				"additional_skills": len(skills['additional_skills']),
				"total_skills": len(skills['matched_facets']) + len(skills['additional_skills'])
			}
		}
        
		# Write JSON file
		json_filename = html_file.stem + '.json'
		json_path = html_file.parent / json_filename
        
		with open(json_path, 'w') as f:
			json.dump(output, f, indent=2)
        
		print(f"   ✓ {len(skills['matched_facets'])} matched facets, {len(skills['additional_skills'])} additional skills")
		print(f"   ✓ Saved to {json_filename}\n")


if __name__ == '__main__':
	main()

