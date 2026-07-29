#!/usr/bin/env python
# Copyright (C) 2026 Sur Herrera Paredes, Mariana Abigail Montante Arenas

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# To see the GNU General Public License, please visit
# <http://www.gnu.org/licenses/>.

from comets_functions import media, load_strains, set_sim_params
import cometspy as c
import os
import argparse

def process_arguments():
    # Read arguments
    parser_format = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=parser_format)
    required = parser.add_argument_group("Required arguments")

    # Define description
    parser.description = ("This simulates communities in a flask using COMETS"
                          "via COMETSPY. The user needs to provide the GEMs"
                          "of the strains in the community, the media name"
                          "and its dilution, and the simulation parameters."
                          "The output is a set of files containing the biomass,"
                          "fluxes, media composition, and total biomass over time.")


    required.add_argument("--gem_path",
                          help=("Path to the folder containing the GEMs"
                                "in SMBL format"),
                          required=True, type=str)
    required.add_argument("--strains",
                          help=("List of strain identifiers corresponding to the GEMs."
                                "Example: --strains ST00042 ST00046"),
                          required=True, nargs='+', type=str)

   

    # # Define other arguments
    parser.add_argument("--outdir",
                        help=("Relative path of directory to create and store output."
                              "Must NOT exist, and it MUST BE a **relative path**"),
                        type=str,
                        default='output')
    parser.add_argument("--media",
                        help="Name of the media to use. Supported: 'lb', 'mm'",
                        type=str,
                        default='lb')
    parser.add_argument("--media_dil",
                        help="Dilution factor for the media. Example: 0.1 for 1/10 dilution.",
                        type=float,
                        default=1)
    parser.add_argument("--media_vol",
                         help="Volume of media to use.",
                         type=float,
                         default=1)
    parser.add_argument("--initial_mass",
                        help=("Initial mass for each strain in grams of dry weight. Example: 1e-8"
                              "Currently, only identical starting masses for all strains are supported."),
                        type=float,
                        default=1e-8)
    parser.add_argument("--ignore_trace_metabolites",
                        help=("Whether to ignore typical trace metabolites in the media."
                              "These are added at a concentration of 1000 mmol/gDW."
                              "If set, only the specified media components will be added,"
                              "otherwise, trace metabolites will be added in addition to"
                              "the specified media components (default)."),
                        action='store_true')
    parser.add_argument("--threads",
                        help="Number of threads to use for the simulation.",
                        type=int,
                        default=4)
    parser.add_argument("--cycles",
                        help="Number of cycles to run the simulation for. Each cycle is a time step of 0.1 hr.",
                        type=int,
                        default=1000)
    parser.add_argument("--gem_suffix",
                        help="Suffix for the GEM files. GEM files will be expected to be named as {gem_path}/{strain_id}{gem_suffix}.",
                        type=str,
                        default='.xml')
    
    args = parser.parse_args()

    return args

if __name__ == "__main__":

    # Read command line arguments
    args = process_arguments()

    # In the future we can do something more fancy with layout
    layout = c.layout()

    # Dictionary of strains and their corresponding GEM paths
    models = dict()
    for strain in args.strains:
        gem_file = os.path.join(args.gem_path, f"{strain}{args.gem_suffix}")
        if not os.path.isfile(gem_file):
            raise FileNotFoundError(f"GEM file for strain {strain} not found at {gem_file}")            
        models[strain] = gem_file

    # Load models into the layout
    layout = load_strains(layout, models, initial_mass=args.initial_mass)    

    # Set media
    if not args.ignore_trace_metabolites:
        layout.add_typical_trace_metabolites(amount=1000)
    
    for metabolite, amount in media(args.media, dil = args.media_dil, vol=args.media_vol).items():
        layout.set_specific_metabolite(metabolite, amount)
            
    # Set simulation parameters.
    sim_params = set_sim_params(args)
    # print(sim_params.show_params().to_string())

    # Create output directory, error if already exists
    if os.path.exists(args.outdir):
        raise FileExistsError(f"Output directory {args.outdir} already exists. Please choose a different name or remove it.") 
    os.makedirs(args.outdir)
    os.makedirs(os.path.join(args.outdir, "sim/"))

    # Prepare simulation
    sim = c.comets(layout = layout, parameters = sim_params, relative_dir=os.path.join(args.outdir, "sim/")) # Needs the final '/'!!
    # Very ugly, but I need to redefine the output filenames
    # https://github.com/segrelab/cometspy/issues/64
    # Even uglier, but the use construction of relative paths by cometspy is really bad
    sim.parameters.set_param("BiomassLogName", "../biomass.txt")
    sim.parameters.set_param("FluxLogName", "../flux.txt")
    sim.parameters.set_param("MediaLogName", "../media.txt")
    sim.parameters.set_param("TotalBiomassLogName","../total_biomass.txt")
    sim.parameters.set_param("velocityMultiConvLogName", ".../velocity.txt")

    print("Starting simulation...")
    sim.run(delete_files=False)
    # print(sim.run_output)
    # print(sim.run_errors)

    # Finally, we write the exchange fluxes for all models
    for model_id in sim.layout.get_model_ids():
        Fluxes_ex = sim.get_species_exchange_fluxes(model_id)
        Fluxes_ex.to_csv(os.path.join(args.outdir, f"{model_id}_exchange_fluxes.tsv"), sep="\t", index=False)

    
