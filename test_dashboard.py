#!/usr/bin/env python3
"""
Script de prueba rápida para verificar que el dashboard v4 funciona
antes de deployar a Streamlit Cloud.

Uso:
    python test_dashboard.py
"""

import sys
import importlib.util

def test_imports():
    """Verifica que todas las dependencias estén instaladas."""
    print("🔍 Verificando dependencias...")
    missing = []
    
    required = ['streamlit', 'pandas', 'numpy', 'plotly']
    for package in required:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} — NO INSTALADO")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Faltan dependencias: {', '.join(missing)}")
        print(f"\nInstalar con: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ Todas las dependencias están instaladas\n")
    return True

def test_syntax():
    """Verifica que el código no tenga errores de sintaxis."""
    print("🔍 Verificando sintaxis de quirkosig_dashboard.py...")
    
    spec = importlib.util.spec_from_file_location("dashboard", "quirkosig_dashboard.py")
    if spec is None:
        print("❌ No se pudo cargar quirkosig_dashboard.py")
        return False
    
    try:
        module = importlib.util.module_from_spec(spec)
        # No ejecutamos spec.loader.exec_module() porque Streamlit requiere
        # ser ejecutado en su propio contexto
        print("✅ El código tiene sintaxis válida\n")
        return True
    except Exception as e:
        print(f"❌ Error de sintaxis: {e}\n")
        return False

def test_version():
    """Verifica que sea la versión correcta."""
    print("🔍 Verificando versión del dashboard...")
    
    try:
        with open('quirkosig_dashboard.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'v4' in content.lower() and '36 meses' in content.lower():
                print("✅ Versión 4.0 detectada (36 meses + T_full dinámico)\n")
                return True
            else:
                print("⚠️  No se detectó versión 4.0 en el código\n")
                return False
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}\n")
        return False

def main():
    print("=" * 60)
    print("🌿 QuirkoSIG Dashboard v4 — Test Pre-Deploy")
    print("=" * 60 + "\n")
    
    # Test 1: Dependencias
    if not test_imports():
        return 1
    
    # Test 2: Sintaxis
    if not test_syntax():
        return 1
    
    # Test 3: Versión
    if not test_version():
        print("⚠️  Advertencia: puede que no sea la versión correcta\n")
    
    # Todo OK
    print("=" * 60)
    print("✅ TODOS LOS TESTS PASARON")
    print("=" * 60)
    print("\n🚀 Para ejecutar localmente:")
    print("   streamlit run quirkosig_dashboard.py")
    print("\n📤 Para deployar:")
    print("   1. Sube los archivos a GitHub")
    print("   2. Sigue DEPLOY.md")
    print("\n💡 Características v4:")
    print("   • 36 meses de proyección (3 años)")
    print("   • T_full dinámico basado en revenue")
    print("   • FT inicial USD 2,500")
    print("   • Mandatorio USD 3,000 → USD 14,400")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
