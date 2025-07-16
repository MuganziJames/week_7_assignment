#!/usr/bin/env python3
"""
COMPAS Dataset Bias Audit Script
AI Ethics Assignment - Week 7

This script performs a comprehensive bias audit of the COMPAS recidivism dataset
using AI Fairness 360 and other fairness analysis tools.

Author: [Your Name]
Date: July 16, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class COMPASBiasAuditor:
    """
    A comprehensive bias auditor for the COMPAS dataset
    """
    
    def __init__(self, data_source='aif360'):
        """
        Initialize the auditor with data source
        
        Args:
            data_source (str): 'aif360' or 'propublica' for data source
        """
        self.data_source = data_source
        self.df = None
        self.fairness_metrics = {}
        self.di_results = {}
        self.predictive_results = {}
        
    def load_data(self):
        """Load COMPAS dataset from specified source"""
        try:
            if self.data_source == 'aif360':
                from aif360.datasets import CompasDataset
                dataset = CompasDataset()
                self.df = dataset.convert_to_dataframe()[0]
                print("✅ COMPAS dataset loaded from AIF360")
            else:
                # Load from ProPublica GitHub
                url = "https://raw.githubusercontent.com/propublica/compas-analysis/master/compas-scores-two-years.csv"
                self.df = pd.read_csv(url)
                print("✅ COMPAS dataset loaded from ProPublica")
                
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            print("Attempting alternative loading method...")
            
            # Fallback to ProPublica source
            try:
                url = "https://raw.githubusercontent.com/propublica/compas-analysis/master/compas-scores-two-years.csv"
                self.df = pd.read_csv(url)
                print("✅ Dataset loaded from ProPublica (fallback)")
            except Exception as e2:
                print(f"❌ Failed to load dataset: {e2}")
                return False
                
        return True
    
    def preprocess_data(self):
        """Preprocess the dataset for analysis"""
        if self.df is None:
            print("❌ No data loaded")
            return False
            
        # Ensure required columns exist
        required_columns = ['race', 'two_year_recid', 'decile_score']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            return False
            
        # Create binary high-risk indicator
        self.df['high_risk'] = (self.df['decile_score'] >= 7).astype(int)
        
        # Clean data
        self.df = self.df.dropna(subset=required_columns)
        
        print(f"✅ Data preprocessed. Shape: {self.df.shape}")
        return True
    
    def calculate_fairness_metrics(self):
        """Calculate comprehensive fairness metrics"""
        metrics = {}
        
        for race in self.df['race'].unique():
            race_data = self.df[self.df['race'] == race]
            
            # Basic statistics
            total_count = len(race_data)
            recid_rate = race_data['two_year_recid'].mean()
            high_risk_rate = race_data['high_risk'].mean()
            avg_score = race_data['decile_score'].mean()
            
            # Confusion matrix components
            tp = len(race_data[(race_data['high_risk'] == 1) & (race_data['two_year_recid'] == 1)])
            fp = len(race_data[(race_data['high_risk'] == 1) & (race_data['two_year_recid'] == 0)])
            tn = len(race_data[(race_data['high_risk'] == 0) & (race_data['two_year_recid'] == 0)])
            fn = len(race_data[(race_data['high_risk'] == 0) & (race_data['two_year_recid'] == 1)])
            
            # Calculate fairness metrics
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
            fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
            tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            
            metrics[race] = {
                'count': total_count,
                'recidivism_rate': recid_rate,
                'high_risk_rate': high_risk_rate,
                'avg_score': avg_score,
                'false_positive_rate': fpr,
                'false_negative_rate': fnr,
                'true_positive_rate': tpr,
                'precision': precision
            }
        
        self.fairness_metrics = metrics
        return metrics
    
    def calculate_disparate_impact(self):
        """Calculate disparate impact ratios"""
        rates = self.df.groupby('race')['high_risk'].mean()
        max_rate = rates.max()
        
        di_results = {}
        for race, rate in rates.items():
            di_ratio = rate / max_rate if max_rate > 0 else 0
            di_results[race] = {
                'rate': rate,
                'di_ratio': di_ratio,
                'passes_80_rule': di_ratio >= 0.8
            }
        
        self.di_results = di_results
        return di_results
    
    def analyze_predictive_performance(self):
        """Analyze predictive performance across groups"""
        from sklearn.metrics import roc_auc_score
        
        results = {}
        self.df['predicted_high_risk'] = self.df['high_risk']
        
        for race in self.df['race'].unique():
            race_data = self.df[self.df['race'] == race]
            
            if len(race_data) > 10:
                # Calculate AUC
                auc = roc_auc_score(race_data['two_year_recid'], race_data['decile_score'])
                
                # Calculate calibration
                high_risk_subset = race_data[race_data['predicted_high_risk'] == 1]
                calibration = high_risk_subset['two_year_recid'].mean() if len(high_risk_subset) > 0 else 0
                
                results[race] = {
                    'sample_size': len(race_data),
                    'auc_score': auc,
                    'calibration': calibration
                }
        
        self.predictive_results = results
        return results
    
    def perform_statistical_tests(self):
        """Perform statistical significance tests"""
        # Get top two racial groups by size
        race_counts = self.df['race'].value_counts()
        top_races = race_counts.head(2).index.tolist()
        
        group1_data = self.df[self.df['race'] == top_races[0]]
        group2_data = self.df[self.df['race'] == top_races[1]]
        
        results = {}
        
        # Test difference in COMPAS scores
        score_stat, score_p = stats.mannwhitneyu(
            group1_data['decile_score'], 
            group2_data['decile_score'], 
            alternative='two-sided'
        )
        
        results['score_difference'] = {
            'groups_compared': f"{top_races[0]} vs {top_races[1]}",
            'statistic': score_stat,
            'p_value': score_p,
            'significant': score_p < 0.05
        }
        
        # Test difference in high-risk classification rates
        high_risk_stat, high_risk_p = stats.chi2_contingency([
            [group1_data['high_risk'].sum(), len(group1_data) - group1_data['high_risk'].sum()],
            [group2_data['high_risk'].sum(), len(group2_data) - group2_data['high_risk'].sum()]
        ])[0:2]
        
        results['classification_difference'] = {
            'groups_compared': f"{top_races[0]} vs {top_races[1]}",
            'statistic': high_risk_stat,
            'p_value': high_risk_p,
            'significant': high_risk_p < 0.05
        }
        
        return results
    
    def create_visualizations(self, save_path='results/'):
        """Create comprehensive visualizations"""
        import os
        os.makedirs(save_path, exist_ok=True)
        
        # 1. Overview visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('COMPAS Dataset Bias Analysis Overview', fontsize=16, fontweight='bold')
        
        # Race distribution
        race_counts = self.df['race'].value_counts()
        axes[0, 0].pie(race_counts.values, labels=race_counts.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Distribution by Race')
        
        # Recidivism by race
        recid_by_race = self.df.groupby('race')['two_year_recid'].mean()
        axes[0, 1].bar(recid_by_race.index, recid_by_race.values, color='coral')
        axes[0, 1].set_title('Recidivism Rate by Race')
        axes[0, 1].set_ylabel('Recidivism Rate')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # COMPAS scores by race
        sns.boxplot(data=self.df, x='race', y='decile_score', ax=axes[1, 0])
        axes[1, 0].set_title('COMPAS Scores by Race')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Score distribution
        axes[1, 1].hist(self.df['decile_score'], bins=10, edgecolor='black', alpha=0.7)
        axes[1, 1].set_title('Distribution of COMPAS Scores')
        axes[1, 1].set_xlabel('Decile Score')
        axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig(f'{save_path}compas_overview.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Fairness metrics visualization
        if self.fairness_metrics:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Fairness Metrics by Race', fontsize=16, fontweight='bold')
            
            races = list(self.fairness_metrics.keys())
            
            # False Positive Rates
            fpr_values = [self.fairness_metrics[race]['false_positive_rate'] for race in races]
            axes[0, 0].bar(races, fpr_values, color='coral')
            axes[0, 0].set_title('False Positive Rate by Race')
            axes[0, 0].set_ylabel('False Positive Rate')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # False Negative Rates
            fnr_values = [self.fairness_metrics[race]['false_negative_rate'] for race in races]
            axes[0, 1].bar(races, fnr_values, color='lightblue')
            axes[0, 1].set_title('False Negative Rate by Race')
            axes[0, 1].set_ylabel('False Negative Rate')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # High Risk Rates
            hr_values = [self.fairness_metrics[race]['high_risk_rate'] for race in races]
            axes[1, 0].bar(races, hr_values, color='lightgreen')
            axes[1, 0].set_title('High Risk Classification Rate by Race')
            axes[1, 0].set_ylabel('High Risk Rate')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # Average Scores
            avg_scores = [self.fairness_metrics[race]['avg_score'] for race in races]
            axes[1, 1].bar(races, avg_scores, color='gold')
            axes[1, 1].set_title('Average COMPAS Score by Race')
            axes[1, 1].set_ylabel('Average Score')
            axes[1, 1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig(f'{save_path}fairness_metrics.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        # 3. Disparate Impact visualization
        if self.di_results:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            groups = list(self.di_results.keys())
            rates = [self.di_results[group]['rate'] for group in groups]
            di_ratios = [self.di_results[group]['di_ratio'] for group in groups]
            colors = ['red' if not self.di_results[group]['passes_80_rule'] else 'green' for group in groups]
            
            # High-risk rates
            ax1.bar(groups, rates, color=colors, alpha=0.7)
            ax1.set_title('High-Risk Classification Rates by Race')
            ax1.set_ylabel('High-Risk Rate')
            ax1.tick_params(axis='x', rotation=45)
            
            # Disparate impact ratios
            ax2.bar(groups, di_ratios, color=colors, alpha=0.7)
            ax2.set_title('Disparate Impact Ratios')
            ax2.set_ylabel('DI Ratio')
            ax2.tick_params(axis='x', rotation=45)
            ax2.axhline(y=0.8, color='orange', linestyle='--', label='80% Rule')
            ax2.axhline(y=1.0, color='blue', linestyle='-', alpha=0.5, label='Parity')
            ax2.legend()
            
            plt.tight_layout()
            plt.savefig(f'{save_path}disparate_impact.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def generate_report(self):
        """Generate comprehensive bias audit report"""
        report_lines = []
        report_lines.append("# COMPAS Dataset Bias Audit Report")
        report_lines.append("Generated by AI Ethics Assignment Analysis")
        report_lines.append(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("## Executive Summary")
        total_samples = len(self.df)
        racial_groups = self.df['race'].nunique()
        overall_recid_rate = self.df['two_year_recid'].mean()
        
        report_lines.append(f"- **Total samples analyzed:** {total_samples:,}")
        report_lines.append(f"- **Racial groups:** {racial_groups}")
        report_lines.append(f"- **Overall recidivism rate:** {overall_recid_rate:.1%}")
        report_lines.append("")
        
        # Key Findings
        report_lines.append("## Key Findings")
        
        # Disparate Impact
        failing_groups = [group for group, result in self.di_results.items() if not result['passes_80_rule']]
        if failing_groups:
            report_lines.append("### ⚠️ Disparate Impact Detected")
            report_lines.append(f"Groups failing 80% rule: {', '.join(failing_groups)}")
            for group in failing_groups:
                ratio = self.di_results[group]['di_ratio']
                report_lines.append(f"- **{group}:** {ratio:.3f} ratio ({(1-ratio)*100:.1f}% below parity)")
        else:
            report_lines.append("### ✅ Disparate Impact: All groups pass 80% rule")
        
        report_lines.append("")
        
        # False Positive Rate Analysis
        fpr_values = [metrics['false_positive_rate'] for metrics in self.fairness_metrics.values()]
        fpr_range = max(fpr_values) - min(fpr_values)
        report_lines.append("### False Positive Rate Disparity")
        report_lines.append(f"- **Range across groups:** {fpr_range:.3f}")
        if fpr_range > 0.1:
            report_lines.append("- ⚠️ **Significant disparity detected** (>10% difference)")
        report_lines.append("")
        
        # Recommendations
        report_lines.append("## Recommendations")
        report_lines.append("### Immediate Actions")
        if failing_groups or fpr_range > 0.1:
            report_lines.append("1. **Implement fairness constraints** in model training")
            report_lines.append("2. **Audit training data** for historical bias patterns")
            report_lines.append("3. **Establish human oversight** for high-risk classifications")
            report_lines.append("4. **Monitor bias metrics** on an ongoing basis")
        else:
            report_lines.append("1. **Continue monitoring** current fairness levels")
            report_lines.append("2. **Establish regular auditing** procedures")
        
        report_lines.append("")
        report_lines.append("### Long-term Improvements")
        report_lines.append("1. **Diversify training data** to ensure representation")
        report_lines.append("2. **Implement fairness-aware algorithms**")
        report_lines.append("3. **Engage stakeholders** in system design")
        report_lines.append("4. **Enhance transparency** and explainability")
        report_lines.append("")
        
        # Technical Details
        report_lines.append("## Technical Details")
        report_lines.append("- **High-risk threshold:** Decile score ≥ 7")
        report_lines.append("- **Fairness metrics:** FPR, FNR, TPR, Disparate Impact")
        report_lines.append("- **Statistical tests:** Mann-Whitney U, Chi-square")
        report_lines.append("- **Tools used:** Python, Pandas, SciPy, Matplotlib")
        
        return "\n".join(report_lines)
    
    def run_complete_audit(self):
        """Run the complete bias audit process"""
        print("🔍 Starting COMPAS Bias Audit...")
        print("=" * 50)
        
        # Load and preprocess data
        if not self.load_data():
            return False
            
        if not self.preprocess_data():
            return False
        
        # Perform analysis
        print("\n📊 Calculating fairness metrics...")
        self.calculate_fairness_metrics()
        
        print("📈 Analyzing disparate impact...")
        self.calculate_disparate_impact()
        
        print("🎯 Evaluating predictive performance...")
        self.analyze_predictive_performance()
        
        print("📊 Performing statistical tests...")
        test_results = self.perform_statistical_tests()
        
        # Generate outputs
        print("\n🎨 Creating visualizations...")
        self.create_visualizations()
        
        print("📄 Generating report...")
        report = self.generate_report()
        
        # Save report
        with open('results/compas_bias_audit_report.md', 'w') as f:
            f.write(report)
        
        # Display summary
        print("\n" + "=" * 50)
        print("✅ BIAS AUDIT COMPLETED")
        print("=" * 50)
        
        # Key findings summary
        failing_groups = [group for group, result in self.di_results.items() if not result['passes_80_rule']]
        if failing_groups:
            print(f"⚠️  BIAS DETECTED: {', '.join(failing_groups)} fail 80% rule")
        else:
            print("✅ All groups pass disparate impact threshold")
        
        fpr_values = [metrics['false_positive_rate'] for metrics in self.fairness_metrics.values()]
        fpr_range = max(fpr_values) - min(fpr_values)
        if fpr_range > 0.1:
            print(f"⚠️  SIGNIFICANT FPR DISPARITY: {fpr_range:.3f} range")
        
        print("\n📁 Files generated:")
        print("- results/compas_overview.png")
        print("- results/fairness_metrics.png") 
        print("- results/disparate_impact.png")
        print("- results/compas_bias_audit_report.md")
        
        return True


def main():
    """Main execution function"""
    auditor = COMPASBiasAuditor(data_source='propublica')
    success = auditor.run_complete_audit()
    
    if success:
        print("\n🎉 Audit completed successfully!")
        print("\nNext steps:")
        print("1. Review generated visualizations")
        print("2. Read the detailed report")
        print("3. Consider implementing recommended mitigations")
    else:
        print("\n❌ Audit failed. Please check error messages above.")


if __name__ == "__main__":
    main()
