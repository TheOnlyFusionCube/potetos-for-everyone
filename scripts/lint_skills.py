#!/usr/bin/env python3
from pathlib import Path, PurePosixPath, PureWindowsPath
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
SKILLS=ROOT/'skills'
errors=[]
inventory=json.loads((ROOT/'UPSTREAM_INVENTORY.json').read_text(encoding='utf-8'))
required_skills=set(inventory['public_skills']) | set(inventory['principles'])
required_playbooks=set(inventory['poteto_mode_playbooks'])
# Vendor primitives are banned only in canonical skill bodies. Ordinary words such as Cursor may appear when crediting provenance.
banned=[r'~/.cursor',r'/add-plugin',r'\bAskQuestion\b',r'\bsubagent_type\b',r'\brun_in_background\b',r'\bTask\s*\(']
for d in sorted(SKILLS.iterdir()):
    if not d.is_dir(): continue
    f=d/'SKILL.md'
    if not f.exists():
        errors.append(f'{d}: missing SKILL.md'); continue
    text=f.read_text(encoding='utf-8')
    m=re.match(r'^---\n(.*?)\n---\n',text,re.S)
    if not m:
        errors.append(f'{f}: invalid/missing frontmatter'); continue
    fm=m.group(1)
    nm=re.search(r'^name:\s*(.+?)\s*$',fm,re.M)
    ds=re.search(r'^description:\s*(.+?)\s*$',fm,re.M)
    if not nm or nm.group(1)!=d.name: errors.append(f'{f}: name must equal directory')
    if not ds or not ds.group(1).strip(): errors.append(f'{f}: description required')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',d.name): errors.append(f'{d.name}: invalid Agent Skills name')
    for pat in banned:
        if re.search(pat,text): errors.append(f'{f}: vendor-specific primitive matches {pat}')
actual_skills={p.name for p in SKILLS.iterdir() if p.is_dir() and (p/'SKILL.md').exists()}
missing_skills=required_skills-actual_skills
extra_skills=actual_skills-required_skills
if missing_skills: errors.append('missing upstream-equivalent skills: '+', '.join(sorted(missing_skills)))
if extra_skills: errors.append('unexpected canonical skills not in tracked upstream inventory: '+', '.join(sorted(extra_skills)))
playdir=SKILLS/'poteto-mode'/'playbooks'
found={p.stem for p in playdir.glob('*.md')}
missing=required_playbooks-found
extra=found-required_playbooks
if missing: errors.append('missing playbooks: '+', '.join(sorted(missing)))
if extra: errors.append('unexpected playbooks not in tracked upstream inventory: '+', '.join(sorted(extra)))

def unsafe_destination(raw):
    # Reject traversal and absolute or drive-relative paths on both Unix and Windows.
    if not isinstance(raw, str) or not raw or any(ch in raw for ch in ('\\', ':', '\x00')):
        return True
    return any(p.anchor or not p.parts or '..' in p.parts
               for p in (PurePosixPath(raw), PureWindowsPath(raw)))

registry=json.loads((ROOT/'adapters'/'registry.json').read_text(encoding='utf-8'))
required_adapters={'generic','universal','cursor','claude','codex','gemini','copilot','windsurf','cline','roo','continue','kiro'}
missing_adapters=required_adapters-set(registry)
if missing_adapters: errors.append('missing adapters: '+', '.join(sorted(missing_adapters)))
for name,spec in registry.items():
    expected_skill_dir = '.kiro/skills' if name == 'kiro' else '.agents/skills'
    if spec.get('skill_dir') != expected_skill_dir:
        errors.append(f'adapter {name}: skill_dir must be {expected_skill_dir}')
    for field in ('skill_dir', 'instruction_file'):
        if unsafe_destination(spec.get(field)):
            errors.append(f'adapter {name}: unsafe {field}')

lic=(ROOT/'LICENSE').read_text(encoding='utf-8'); notice=(ROOT/'NOTICE.md').read_text(encoding='utf-8'); readme=(ROOT/'README.md').read_text(encoding='utf-8')
for label,text in [('LICENSE',lic),('NOTICE',notice),('README',readme)]:
    if 'Lauren Tan' not in text: errors.append(f'{label}: Lauren Tan attribution missing')
if 'Copyright (c) 2026 Lauren Tan' not in lic: errors.append('LICENSE: upstream copyright notice missing')
if errors:
    print('\n'.join('ERROR: '+e for e in errors),file=sys.stderr); raise SystemExit(1)
print(f'ok: {sum(1 for p in SKILLS.iterdir() if (p/"SKILL.md").exists())} skills, {len(found)} playbooks')
