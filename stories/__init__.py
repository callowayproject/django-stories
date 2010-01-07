import os, sys
diff_match_patch_path = os.path.abspath(
                            os.path.join(
                                os.path.dirname(__file__),
                                'lib',
                                'div_match_patch_20091012',
                                'python'))
sys.path.append(diff_match_patch_path)
