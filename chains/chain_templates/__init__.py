"""
Chain Templates Module
Author: Victor Ibhafidon

Provides pre-built attack chain templates for all supported targets.

This module aggregates templates from all target-specific template files,
making it easy to access templates for any target.

USAGE:
 from chains.chain_templates import get_all_templates, get_templates_by_target
 
 # Get all templates
 all_templates = get_all_templates()
 
 # Get templates for specific target
 juice_templates = get_templates_by_target("juice-shop")
"""

import sys
import os

# Add chains directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from chains.chain_templates.juice_shop_templates import get_juice_shop_templates
from chains.chain_templates.dvwa_templates import get_dvwa_templates
from chains.chain_templates.bwapp_templates import get_bwapp_templates
from chains.chain_templates.iotgoat_templates import get_iotgoat_templates
from chains.chain_templates.robotics_templates import get_robotics_templates

def get_all_templates():
 """
 Get all attack chain templates from all targets.
 
 Returns:
 List of tuples (analyzer, chain) for all templates
 """
 all_templates = []
 
 # Juice Shop templates
 all_templates.extend(get_juice_shop_templates())
 
 # DVWA templates
 all_templates.extend(get_dvwa_templates())
 
 # bWAPP templates
 all_templates.extend(get_bwapp_templates())
 
 # IoTGoat templates
 all_templates.extend(get_iotgoat_templates())
 
 # Robotics templates
 all_templates.extend(get_robotics_templates())
 
 return all_templates

def get_templates_by_target(target_name: str):
 """
 Get templates for a specific target.
 
 Args:
 target_name: Name of target ("juice-shop", "dvwa", "bwapp", "iotgoat", "robotics")
 
 Returns:
 List of tuples (analyzer, chain) for the target
 """
 target_map = {
 "juice-shop": get_juice_shop_templates,
 "juiceshop": get_juice_shop_templates,
 "dvwa": get_dvwa_templates,
 "bwapp": get_bwapp_templates,
 "iotgoat": get_iotgoat_templates,
 "robotics": get_robotics_templates,
 }
 
 target_name_lower = target_name.lower().replace("_", "-")
 
 if target_name_lower in target_map:
 return target_map[target_name_lower]()
 else:
 return []

if __name__ == "__main__":
 print("=" * 80)
 print("CHAIN TEMPLATES - ALL TARGETS")
 print("=" * 80)
 print()
 
 all_templates = get_all_templates()
 
 print(f"Total Templates: {len(all_templates)}")
 print()
 
 # Group by target
 targets = {
 "Juice Shop": len(get_juice_shop_templates()),
 "DVWA": len(get_dvwa_templates()),
 "bWAPP": len(get_bwapp_templates()),
 "IoTGoat": len(get_iotgoat_templates()),
 "Robotics": len(get_robotics_templates()),
 }
 
 print("Templates by Target:")
 for target, count in targets.items():
 print(f" {target}: {count} templates")
 
 print()
 print("=" * 80)

